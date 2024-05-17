#![deny(clippy::all)]
#![deny(clippy::pedantic)]

use block_file::BlockFile;
use easy_fs::{BlockDevice, EasyFileSystem, Inode};
use rand::seq::SliceRandom;
use std::{
    fs::{read_dir, File, OpenOptions},
    io::{Read, Result},
    path::Path,
    sync::{Arc, Mutex},
};

mod block_file;

fn main() -> Result<()> {
    let block_file: Arc<dyn BlockDevice> = Arc::new(BlockFile(Mutex::new({
        let f = OpenOptions::new()
            .read(true)
            .write(true)
            .create(true)
            .truncate(true)
            .open("fs.img")?;
        f.set_len(16 * 2048 * 512)?;
        f
    })));

    let efs = EasyFileSystem::create(&block_file, 16 * 2048, 1);
    let root_inode = Arc::new(EasyFileSystem::root_inode(&efs));
    root_inode.set_default_dirent(root_inode.inode_id());

    let buf = [0xaa; 14 << 10];
    let mut file_names = vec![];

    for i in 0..128 {
        let filename = format!("file_{i:03}");
        file_names.push(filename.clone());
        let inode = root_inode.create(&filename).unwrap();
        inode.write_at(0, &buf);
    }

    let mut rng = rand::thread_rng();
    file_names.shuffle(&mut rng);

    for filename in &file_names[0..64] {
        root_inode.delete(filename);
    }

    let mut file = File::open("flag.png")?;
    let flag = root_inode.create("flag.png").unwrap();

    let mut buf = vec![];
    file.read_to_end(&mut buf).unwrap();
    flag.write_at(0, &buf);

    for filename in &file_names[64..128] {
        root_inode.delete(filename);
    }

    pack_directory(&root_inode, Path::new("../easy-fs-root/"))?;

    Ok(())
}

fn pack_directory(parent_inode: &Arc<Inode>, path: &Path) -> Result<()> {
    for entry in read_dir(path)? {
        let entry_path = entry?.path();
        let entry_name = entry_path.file_name().unwrap().to_str().unwrap();

        if entry_name.starts_with('.') {
            continue;
        }

        if entry_path.is_dir() {
            let dir_inode = parent_inode.create_dir(entry_name).unwrap();
            pack_directory(&dir_inode, &entry_path)?;
        } else if entry_path.is_file() {
            let mut file = File::open(&entry_path)?;
            let inode = parent_inode.create(entry_name).unwrap();

            let mut buffer = vec![0; 8 << 20];
            let mut offset = 0;
            loop {
                let bytes_read = file.read(&mut buffer)?;
                if bytes_read == 0 {
                    break;
                }
                inode.write_at(offset, &buffer[..bytes_read]);
                offset += bytes_read;
            }
        }
    }

    Ok(())
}
