import struct

# Only keep these known good data type IDs (as little-endian 2-byte values)
ALLOWED_IDS = {0x0000, 0x0080, 0x0100, 0x0200, 0x0300, 0x0400}

# Input and output file paths
input_path = "project_data/GB_20150520/CSIR_RDI_Sentinel_FB_20150520_V3000.000"
output_path = "project_data/GB_20150520/CSIR_RDI_Sentinel_FB_20150520_V3000.000.export_cleaned.pd0"

def read_uint16(f):
    return struct.unpack("<H", f.read(2))[0]

def read_record(f):
    header = f.read(2)
    if not header:
        return None
    if len(header) < 2:
        return None
    block_id = struct.unpack("<H", header)[0]

    # Read the next 2 bytes: size of block
    size_bytes = f.read(2)
    if len(size_bytes) < 2:
        return None
    block_size = struct.unpack("<H", size_bytes)[0]

    # Read the remaining bytes of the block
    block_data = f.read(block_size - 4)  # subtract 4 bytes already read
    return block_id, header + size_bytes + block_data

def clean_pd0(input_file, output_file):
    with open(input_file, "rb") as fin, open(output_file, "wb") as fout:
        total = 0
        kept = 0
        while True:
            pos = fin.tell()
            result = read_record(fin)
            if result is None:
                break
            block_id, data = result
            total += 1
            if block_id in ALLOWED_IDS:
                fout.write(data)
                kept += 1
            else:
                print(f"Skipping unsupported block ID: 0x{block_id:04x} at byte {pos}")
        print(f"Finished: {kept}/{total} records written")

if __name__ == "__main__":
    clean_pd0(input_path, output_path)
