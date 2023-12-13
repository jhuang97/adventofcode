use std::fs;
use std::error::Error;
extern crate nalgebra as na;
use na::DMatrix;

#[derive(Debug)]
pub enum Reflection {
    Row(i32),
    Col(i32)
}

pub fn find_almost_reflection(m: &DMatrix<i32>) -> Option<Reflection> {
    for i in 0..m.nrows()-1 {
        if deviations(m, i, i+1, true) <= 1 {
            let mut i1 = i;
            let mut i2 = i+1;
            let mut n_almost = 0;
            loop {
                n_almost += deviations(m, i1, i2, true);
                if n_almost > 1 {
                    break;
                }
                if i1 == 0 || i2 == m.nrows()-1 {
                    break;
                }
                i1 -= 1;
                i2 += 1;
            }
            if n_almost == 1 {
                return Some(Reflection::Row((i+1) as i32));
            }
        }
    }
    for i in 0..m.ncols()-1 {
        if deviations(m, i, i+1, false) <= 1 {
            let mut i1 = i;
            let mut i2 = i+1;
            let mut n_almost = 0;
            loop {
                n_almost += deviations(m, i1, i2, false);
                if n_almost > 1 {
                    break;
                }
                if i1 == 0 || i2 == m.ncols()-1 {
                    break;
                }
                i1 -= 1;
                i2 += 1;
            }
            if n_almost == 1 {
                return Some(Reflection::Col((i+1) as i32));
            }
        }
    }
    None
}

pub fn find_reflection(m: &DMatrix<i32>) -> Option<Reflection> {
    // first try rows
    for i in 0..m.nrows()-1 {
        if m.row(i) == m.row(i+1) {
            let mut i1 = i;
            let mut i2 = i+1;
            let mut reflects = true;
            loop {
                if m.row(i1) != m.row(i2) {
                    reflects = false;
                    break;
                }
                if i1 == 0 || i2 == m.nrows()-1 {
                    break;
                }
                i1 -= 1;
                i2 += 1;
            }
            if reflects {
                return Some(Reflection::Row((i+1) as i32));
            }
        }   
    }

    // then try columns
    for i in 0..m.ncols()-1 {
        if m.column(i) == m.column(i+1) {
            let mut i1 = i;
            let mut i2 = i+1;
            let mut reflects = true;
            loop {
                if m.column(i1) != m.column(i2) {
                    reflects = false;
                    break;
                }
                if i1 == 0 || i2 == m.ncols()-1 {
                    break;
                }
                i1 -= 1;
                i2 += 1;
            }
            if reflects {
                return Some(Reflection::Col((i+1) as i32));
            }
        }   
    }
    None
}

pub fn deviations(m: &DMatrix<i32>, i1: usize, i2: usize, rows: bool) -> i32 {
    let diff = if rows {(m.row(i1) - m.row(i2)).abs()} 
        else {(m.column(i1) - m.column(i2)).abs().transpose()};
    
    let mut count1 = 0;
    for x in &diff {
        match *x {
            0 => (),
            1 => count1 += 1,
            _ => return 2,
        }
    }
    count1
}

pub fn answer(matrices: &Vec<DMatrix<i32>>, f: &dyn Fn(&DMatrix<i32>) -> Option<Reflection>) -> i32 {
    let mut total = 0;
    for m in matrices {
        total += match f(m).unwrap() {
            Reflection::Row(r) => 100*r,
            Reflection::Col(c) => c,
        };
    }
    total
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input13.txt")?;
    let parts: Vec<&str> = input.trim().split("\n\n").collect();
    let mut patterns: Vec<DMatrix<i32>> = Vec::new();

    for p in parts {
        let lines: Vec<_> = p.lines().collect();
        let nr = lines.len();
        let nc = lines[0].len();
        let dm = DMatrix::from_row_iterator(nr, nc, 
            p.chars()
                .filter_map(|c| match c {
                    '#' => Some(1),
                    '.' => Some(0),
                    _ => None
                })
        );
        patterns.push(dm);
    }

    let total = answer(&patterns, &find_reflection);
    dbg!(total);

    let total2 = answer(&patterns, &find_almost_reflection);
    dbg!(total2);

    Ok(())
}