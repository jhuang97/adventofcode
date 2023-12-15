use std::fs;
use std::error::Error;

pub fn get_hash(s: &str) -> u32 {
    let mut curr = 0;
    for c in s.chars() {
        curr += c as u32;
        curr *= 17;
        curr %= 256;
    }
    curr
}

pub struct Lens {
    label: String,
    focal_length: u32,
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input15.txt")?;
    
    let steps: Vec<&str> = input.trim().split(",").collect();

    let total: u32 = (&steps).iter().map(|s| get_hash(s)).sum();
    dbg!(total);

    let mut boxes: Vec<Vec<Lens>> = Vec::new();
    for _ in 0..256 {
        boxes.push(Vec::new());
    }
    for instr in &steps {
        if let Some((label, n_str)) = instr.split_once('=') {
            let focal_length: u32 = n_str.parse()?;
            let idx = get_hash(label);
            let b = &mut boxes[idx as usize];
            if let Some(lens_idx) = b.iter().position(|x| x.label == label) {
                b[lens_idx].focal_length = focal_length;
            } else {
                b.push(Lens {label: label.to_owned(), focal_length});
            }
        } else {
            let (label, _) = instr.split_once('-').unwrap();
            let idx = get_hash(label);
            boxes[idx as usize].retain(|x| x.label != label);
        }
    }

    let mut total2 = 0;
    for (ib, b) in boxes.iter().enumerate() {
        for (il, lens) in b.iter().enumerate() {
            total2 += (ib + 1) * (il + 1) * (lens.focal_length as usize);
        }
    }
    dbg!(total2);

    Ok(())
}
