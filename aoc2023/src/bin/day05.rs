use std::fs;
use std::error::Error;
use std::convert::From;

#[derive(Debug)]
pub struct SeedMapRange {
    dest_start: i64,
    source_start: i64,
    range_len: i64
}

#[derive(Clone, Copy, Debug)]
pub struct Range {
    start: i64,
    len: i64,
}

impl SeedMapRange {
    pub fn apply(&self, n: i64) -> Option<i64> {
        let diff = n - self.source_start;
        if 0 <= diff && diff < self.range_len {
            Some(self.dest_start + diff)
        } else {
            None
        }
    }

    pub fn apply_range(&self, r: Range) -> (Option<Range>, Vec<Range>) {
        let x0 = r.start;
        let x1 = r.start + r.len - 1;
        let d0 = x0 - self.source_start;
        let d1 = x1 - self.source_start;
        if d1 < 0 || d0 >= self.range_len {
            return (None, vec![r]);
        } else {
            let mut mapped_start = self.dest_start + d0;
            let mut n_map = r.len;
            let mut leftovers: Vec<Range> = vec![];
            if d0 < 0 {
                let n_left = -d0;
                n_map -= n_left;
                mapped_start = self.dest_start;
                leftovers.push(Range{start: r.start, len: n_left});
            }
            if d1 >= self.range_len {
                let n_right = d1 - self.range_len + 1;
                let n_not_right = r.len - n_right;
                n_map -= n_right;
                leftovers.push(Range{start: r.start + n_not_right, len: n_right});
            }
            return (Some(Range{start: mapped_start, len: n_map}), leftovers);
        }
    }
}

pub fn apply_map(maps: &Vec<SeedMapRange>, n: i64) -> i64 {
    for m in maps {
        if let Some(out) = m.apply(n) {
            return out;
        }
    }
    n
}

pub fn apply_map_range(maps: &Vec<SeedMapRange>, ranges: &Vec<Range>) -> Vec<Range> {
    let mut mapped: Vec<Range> = vec![];
    let mut unmapped: Vec<Range> = ranges.to_vec();
    for m in maps {
        let mut this_unmapped: Vec<Range> = vec![];
        for r in unmapped.drain(..) {
            let (mapped_range_opt, mut leftovers) = m.apply_range(r);
            if let Some(mapped_range) = mapped_range_opt {
                mapped.push(mapped_range);
                // println!("matched range");
                // dbg!(m);
            }
            this_unmapped.append(&mut leftovers);
        }
        unmapped.append(&mut this_unmapped);
    }
    mapped.append(&mut unmapped);
    mapped
}

impl From<&str> for SeedMapRange {
    fn from(s: &str) -> Self {
        let nums: Vec<i64> = s.split_whitespace().map(|x| x.parse().unwrap()).collect();
        SeedMapRange {
            dest_start: nums[0],
            source_start: nums[1],
            range_len: nums[2]
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input05.txt")?;
    let parts: Vec<&str> = input.trim().split("\n\n").collect();

    let seeds: Vec<i64> = parts[0].split_once(": ").unwrap().1
        .split(" ").map(|x| x.parse().unwrap()).collect();
    
    let seed_maps: Vec<Vec<SeedMapRange>> = parts[1..].iter().map(
        |&s| {
            let map_ranges: Vec<_> = s.split_once(":\n").unwrap().1.split("\n").collect(); 
            map_ranges.iter().map(|&x| SeedMapRange::from(x)).collect::<Vec<_>>()
        }
    ).collect();

    let locations: Vec<i64> = seeds.iter().map(
            |seed| seed_maps.iter().fold(*seed, |acc, m| apply_map(m, acc))
    ).collect();

    let min_loc = locations.iter().min().unwrap();
    dbg!(min_loc);

    let seed_ranges: Vec<Range> = seeds
        .chunks_exact(2)
        .map(|pair| Range{start: pair[0], len: pair[1]}).collect();
    
    let location_ranges: Vec<Range> = seed_maps.iter().fold(seed_ranges, |acc, m| apply_map_range(m, &acc));
    let min_loc2 = location_ranges.iter().map(|r| r.start).min().unwrap();
    // dbg!(location_ranges.len());
    dbg!(min_loc2);

    Ok(())
}