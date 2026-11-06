"""Export supplied SPV outcome encoding and mortality warnings without altering it.

This is a restricted decoder for the two-row simple numeric encoding table in the
supplied SPV, following GNU PSPP's documented light-member Value/Leaf structures.
It is deliberately not a general-purpose SPV parser: unsupported layouts fail.
"""
import hashlib
import json
import re
import struct
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT/'provenance/t04'
MEMBER = '00000000055_lightTableData.bin'


def read_string(data, position):
    length, = struct.unpack_from('<I', data, position)
    end = position+4+length
    if end > len(data):
        raise ValueError('Invalid SPV string length')
    return data[position+4:end].decode('utf-8'), end


def read_leaf_for_label(data, label):
    pattern = b'\x03'+struct.pack('<I', len(label.encode('utf-8')))+label.encode('utf-8')
    locations = [m.start() for m in re.finditer(re.escape(pattern), data)]
    if len(locations) != 1:
        raise ValueError('Expected one exact local category label')
    position = locations[0]+len(pattern)
    if data[position] != 0x58:
        raise ValueError('Unsupported ValueMod')
    _, position = read_string(data, position+1)  # identifier
    canonical, position = read_string(data, position)
    if canonical != label or data[position] not in [0, 1]:
        raise ValueError('Category label/fixed flag mismatch')
    position += 1
    if data[position:position+3] != b'\0\0\0':
        raise ValueError('Unsupported leaf prefix')
    leaf_type, leaf_index, trailing = struct.unpack_from('<III', data, position+3)
    if leaf_type != 2 or trailing != 0:
        raise ValueError('Unsupported leaf structure')
    return leaf_index


def decode_encoding(data):
    # Cells => int32 count, followed by uint64 index and numeric Value entries.
    size = struct.calcsize('<QBBId')
    start = len(data)-(4+2*size)
    count, = struct.unpack_from('<I', data, start)
    if count != 2:
        raise ValueError('Expected exactly two trailing numeric cells')
    values = {}
    for i in range(2):
        index, kind, modifier, number_format, value = struct.unpack_from('<QBBId', data, start+4+i*size)
        if kind != 1 or modifier != 0x58 or value not in [0.0, 1.0] or index in values:
            raise ValueError('Unsupported numeric cell layout')
        values[index] = int(value)
    result = {}
    for label in ['Fallecid', 'Vivo    ']:
        leaf = read_leaf_for_label(data, label)
        result[label.strip()] = dict(leaf_index=leaf, internal_value=values[leaf])
    if set(v['internal_value'] for v in result.values()) != {0, 1}:
        raise ValueError('Encoding is not binary')
    return result


def readable_strings(data):
    result = []
    for part in re.findall(rb'[\x20-\xff]{9,}', data):
        try:
            result.append(part.decode('utf-8'))
        except UnicodeDecodeError:
            result.append(part.decode('cp1252', errors='replace'))
    return result


def main():
    OUT.mkdir(exist_ok=True)
    path = ROOT/'Results/RESULTADOS.spv'
    if not path.exists():
        if not (OUT/'legacy_encoding.json').exists():
            (OUT/'legacy_encoding.json').write_text(json.dumps({'status':'unavailable','reason':'Supplied SPV not restored on this workstation; no encoding inference made'}, indent=2)+'\n', encoding='utf-8')
        print('Legacy SPV not available locally; preserved historical evidence unchanged. Rebuilt death coding does not depend on this file.')
        return
    with zipfile.ZipFile(path) as archive:
        data = archive.read(MEMBER)
        encoding = decode_encoding(data)
        warnings = {}
        for member in ['00000000053_lightWarningData.bin', '000000000582_lightTableData.bin']:
            strings = readable_strings(archive.read(member))
            warnings[member] = [s for s in strings if any(k in s for k in ['8 bytes', 'truncar', 'iteraci', 'soluci'])]
    result = dict(status='decoded', source_path=path.relative_to(ROOT).as_posix(),
                  source_sha256=hashlib.sha256(path.read_bytes()).hexdigest(), member=MEMBER,
                  member_sha256=hashlib.sha256(data).hexdigest(), encoding=encoding,
                  warnings=warnings, interpretation='Internal event=1 is '+next(k for k,v in encoding.items() if v['internal_value']==1),
                  format_reference='https://www.gnu.org/software/pspp/pspp-dev/html_node/index.html')
    (OUT/'legacy_encoding.json').write_text(json.dumps(result, indent=2, ensure_ascii=False)+'\n', encoding='utf-8')
    lines=['# Supplied SPV mortality-model evidence', '', '| Original label (truncated by SPSS) | Internal value |', '|---|---:|']
    for label, row in encoding.items():lines.append(f"| {label} | {row['internal_value']} |")
    lines += ['', 'The fitted event was **live discharge**, not death. This confirms the direction error in the mortality-labelled interpretation. The old model also lacks a converged solution, so reciprocating its printed odds ratios is not a valid repair.', '', '## Saved warning/model-summary text', '']
    for member, strings in warnings.items():
        lines.append(f'Archive member: `{member}`')
        lines.extend(f'- {s}' for s in dict.fromkeys(strings))
        lines.append('')
    lines += ['The restricted binary decoder validates category leaf indices and two numeric cells. It fails on unsupported layouts rather than guessing. Input files remain unchanged.', '']
    (OUT/'legacy_model_evidence.md').write_text('\n'.join(lines), encoding='utf-8')
    print(json.dumps(encoding, ensure_ascii=False))

if __name__ == '__main__':main()
