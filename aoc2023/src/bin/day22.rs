use std::collections::{HashSet, HashMap};
use std::fs;
use std::error::Error;
use std::ops::RangeInclusive;

#[derive(Debug)]
enum Block {
    LineX(RangeInclusive<i32>, i32, i32),
    LineY(i32, RangeInclusive<i32>, i32),
    LineZ(i32, i32, RangeInclusive<i32>),
}

impl Block {
    fn footprint(&self) -> i32 {
        match self {
            Block::LineX(xr, _, _) => xr.end() - xr.start() + 1,
            Block::LineY(_, yr, _) => yr.end() - yr.start() + 1,
            Block::LineZ(_, _, _) => 1,
        }
    }

    fn zmin(&self) -> i32 {
        match self {
            Block::LineX(_, _, z) => *z,
            Block::LineY(_, _, z) => *z,
            Block::LineZ(_, _, zr) => *zr.start(),
        }
    }

    fn lower(&mut self) {
        match self {
            Block::LineX(_, _, ref mut z) | Block::LineY(_, _, ref mut z) => *z -= 1,
            Block::LineZ(_, _, ref mut zr) => *zr = *zr.start()-1..=*zr.end()-1,
        }
    }
}

fn parse_block(s: &str) -> Block {
    let nums: Vec<i32> = s.split([',', '~']).map(|x| x.parse().unwrap()).collect();
    assert!(nums.len() == 6);
    let (x1, y1, z1, x2, y2, z2) = (nums[0], nums[1], nums[2], nums[3], nums[4], nums[5]);
    if x1 != x2 {
        Block::LineX(x1..=x2, y1, z1)
    } else if y1 != y2 {
        Block::LineY(x1, y1..=y2, z1)
    } else if z1 != z2 {
        Block::LineZ(x1, y1, z1..=z2)
    } else {
        Block::LineX(x1..=x2, y1, z1)
    }
}

fn make_map(v: &Vec<Block>) -> HashMap<(i32, i32, i32), usize> {
    let mut out = HashMap::new();
    for (i, b) in v.iter().enumerate() {
        match b {
            Block::LineX(xr, y, z) => {
                for x in xr.clone() {
                    out.insert((x, *y, *z), i);
                }
            },
            Block::LineY(x, yr, z) => {
                for y in yr.clone() {
                    out.insert((*x, y, *z), i);
                }
            },
            Block::LineZ(x, y, zr) => {
                for z in zr.clone() {
                    out.insert((*x, *y, z), i);
                }
            },
        }
    }
    out
}

fn fall(b: &mut Block, idx: usize, points: &mut HashMap<(i32, i32, i32), usize>) -> Option<HashSet<usize>> {
    let mut resting_on = HashSet::new();
    while b.zmin() > 1 {
        match b {
            Block::LineX(xr, y, z) => {
                for x in xr.clone() {
                    if let Some(&ib) = points.get(&(x, *y, *z-1)) {
                        resting_on.insert(ib);
                    }
                }
            },
            Block::LineY(x, yr, z) => {
                for y in yr.clone() {
                    if let Some(&ib) = points.get(&(*x, y, *z-1)) {
                        resting_on.insert(ib);
                    }
                }
            },
            Block::LineZ(x, y, zr) => {
                if let Some(&ib) = points.get(&(*x, *y, zr.start()-1)) {
                    resting_on.insert(ib);
                }
            },
        }
        if !resting_on.is_empty() {
            return Some(resting_on);
        }

        // update points
        match b {
            Block::LineX(xr, y, z) => {
                for x in xr.clone() {
                    points.remove(&(x, *y, *z));
                    points.insert((x, *y, *z-1), idx);
                }
            },
            Block::LineY(x, yr, z) => {
                for y in yr.clone() {
                    points.remove(&(*x, y, *z));
                    points.insert((*x, y, *z-1), idx);
                }
            },
            Block::LineZ(x, y, zr) => {
                points.remove(&(*x, *y, *zr.end()));
                points.insert((*x, *y, *zr.start()-1), idx);
            },
        }

        b.lower();
    }
    None
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input22.txt")?;
    // let input = fs::read_to_string("test22.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut blocks: Vec<Block> = lines.iter().map(|x| parse_block(x)).collect();
    blocks.sort_unstable_by_key(|b| (b.zmin(), b.footprint()));

    let mut final_indices: HashSet<usize> = HashSet::new();
    let mut non_final_indices: Vec<usize> = (0..blocks.len()).collect();
    let mut resting_on: HashMap<usize, HashSet<usize>> = HashMap::new();
    let mut supporting: HashMap<usize, HashSet<usize>> = HashMap::new();

    let mut points: HashMap<(i32, i32, i32), usize> = make_map(&blocks);

    while !non_final_indices.is_empty() {
        let idx = non_final_indices[0];
        let fall_idx_opt = fall(&mut blocks[idx], idx, &mut points);
        let mut finalized = false;

        if blocks[idx].zmin() == 1 {
            finalized = true;
        } else if let Some(resting_idx) = fall_idx_opt {
            if resting_idx.iter().any(|ridx| final_indices.contains(ridx)) {
                finalized = true;
            }

            if finalized {
                for ridx in &resting_idx {
                    (*supporting.entry(*ridx).or_insert(HashSet::new())).insert(idx);
                }
                resting_on.insert(idx, resting_idx);
            }
        }

        if finalized {
            non_final_indices.retain(|&x| x != idx);
            final_indices.insert(idx);
        }
    }

    let mut cannot_remove: HashSet<usize> = HashSet::new();
    for (bidx, ridx) in &resting_on {
        if ridx.len() == 1 {
            let ridx1 = *ridx.iter().next().unwrap();
            cannot_remove.insert(ridx1);
        }
    }
    let num_can_remove = blocks.len() - cannot_remove.len();
    dbg!(num_can_remove);

    let n_fall_total: usize = (0..blocks.len()).map(|x| n_fall(x, &resting_on, &supporting)).sum();
    dbg!(n_fall_total);

    Ok(())
}

fn n_fall(idx: usize, resting_on: &HashMap<usize, HashSet<usize>>, supporting: &HashMap<usize, HashSet<usize>>) -> usize {
    if let Some(supported) = supporting.get(&idx) {
        let mut fallen: HashSet<usize> = HashSet::from([idx]);
        let mut need_to_check: Vec<usize> = supported.clone().into_iter().collect();
        while let Some(bidx) = need_to_check.pop() {
            if resting_on.get(&bidx).unwrap()
                .iter()
                .all(|ridx| fallen.contains(ridx))
            {
                fallen.insert(bidx);
                if let Some(b_supported) = supporting.get(&bidx) {
                    need_to_check.extend(b_supported);
                }
            }
        }
        fallen.len() - 1
    } else {
        0
    }
}