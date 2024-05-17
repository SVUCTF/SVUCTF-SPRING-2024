import os
import struct

BLOCK_SIZE = 512
DISK_INODE_SIZE = 128

SUPER_BLOCK_FMT = "<6I488x"
DISK_INODE_FMT = "<B3xI27IIII"
INDIRECT_BLOCK_FMT = "<128I"


def read_indirect_block(indirect_block_index: int, level: int) -> bytes:
    data = b""

    image.seek(indirect_block_index * BLOCK_SIZE)
    indirect_block_data = image.read(BLOCK_SIZE)
    indirect_block_indices = struct.unpack(INDIRECT_BLOCK_FMT, indirect_block_data)

    for index in indirect_block_indices:
        if index == 0:
            break
        if level == 1:
            image.seek(index * BLOCK_SIZE)
            data += image.read(BLOCK_SIZE)
        else:
            data += read_indirect_block(index, level - 1)

    return data


if not os.path.exists("output"):
    os.mkdir("output")


with open("fs.img", "rb") as image:
    image.seek(BLOCK_SIZE)
    inode_bitmap_data = image.read(BLOCK_SIZE)
    inode_bitmap = [byte for byte in inode_bitmap_data]
    inode_indices = [
        index * 8 + bit
        for index, byte in enumerate(inode_bitmap)
        for bit in range(8)
        if byte & (1 << bit) != 0
    ]

    for inode_index in inode_indices:
        image.seek(BLOCK_SIZE * 2 + DISK_INODE_SIZE * inode_index)
        disk_inode_data = image.read(DISK_INODE_SIZE)
        disk_inode = struct.unpack(DISK_INODE_FMT, disk_inode_data)

        file_type = disk_inode[0]
        file_size = disk_inode[1]
        direct_blocks = disk_inode[2:29]
        indirect1_index = disk_inode[29]
        indirect2_index = disk_inode[30]
        indirect3_index = disk_inode[31]

        print(
            inode_index,
            "file" if file_type == 0 else "dir",
            file_size,
            direct_blocks,
            indirect1_index,
            indirect2_index,
            indirect3_index,
        )

        if file_type == 1:
            continue

        file_data = b""

        for block_index in direct_blocks:
            if block_index == 0:
                break
            image.seek(block_index * BLOCK_SIZE)
            file_data += image.read(BLOCK_SIZE)
        if indirect1_index != 0:
            file_data += read_indirect_block(indirect1_index, 1)
        if indirect2_index != 0:
            file_data += read_indirect_block(indirect2_index, 2)
        if indirect3_index != 0:
            file_data += read_indirect_block(indirect3_index, 3)

        file_data = file_data[:file_size]
        file_path = os.path.join("output", f"file{inode_index}")

        with open(file_path, "wb") as file:
            file.write(file_data)
