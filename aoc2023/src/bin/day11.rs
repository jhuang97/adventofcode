use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input11.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    let mut galaxy_r: Vec<i64> = Vec::new();
    let mut galaxy_c: Vec<i64> = Vec::new();
    for r in 0..nr {
        for c in 0..nc {
            if grid[r][c] == '#' {
                galaxy_r.push(r as i64);
                galaxy_c.push(c as i64);
            }
        }
    }
    let dist_tot = dists_1d(&galaxy_r, 1) + dists_1d(&galaxy_c, 1);
    dbg!(dist_tot);

    let dist_tot2 = dists_1d(&galaxy_r, 999999) + dists_1d(&galaxy_c, 999999);
    dbg!(dist_tot2);

    Ok(())
}

pub fn dists_1d(x: &Vec<i64>, dsize: i64) -> i64 {
    let x_max = *x.iter().max().unwrap();
    let mut x_new: Vec<i64> = (0..=x_max).collect();
    for xi in 0..x_max {
        if !x.contains(&xi) {
            for xni in xi+1..=x_max {
                x_new[xni as usize] += dsize;
            }
        }
    }
    let mut total: i64 = 0;
    for i in 0..x.len()-1 {
        for j in i+1..x.len() {
            total += (x_new[x[i] as usize] - x_new[x[j] as usize]).abs();
        }
    }
    total
}