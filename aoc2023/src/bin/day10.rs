use std::fs;
use std::error::Error;
use std::iter::zip;
use std::collections::{HashSet, BTreeSet};

static N: (i32, i32) = (-1, 0);
static S: (i32, i32) = (1, 0);
static E: (i32, i32) = (0, 1);
static W: (i32, i32) = (0, -1);
static DIRS: [(i32, i32); 4] = [N, E, S, W];

pub fn pipe_dir(ch: char) -> Vec<(i32, i32)> {
    match ch {
        '|' => vec![N, S],
        '-' => vec![E, W],
        'L' => vec![N, E],
        'J' => vec![N, W],
        '7' => vec![S, W],
        'F' => vec![S, E],
        '.' => vec![],
        _ => vec![],
    }
}

pub fn find_char(grid: &Vec<Vec<char>>, ch: char) -> Option<(usize, usize)> {
    for r in 0..grid.len() {
        for c in 0..grid[0].len() {
            if grid[r][c] == ch {
                return Some((r, c));
            }
        }
    }
    None
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input10.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    let raw_S = find_char(&grid, 'S').unwrap();
    let rS = raw_S.0 as i32;
    let cS = raw_S.1 as i32;
    
    let S_dirs: Vec<(i32, i32)> = DIRS
        .iter()
        .filter_map(|(dr, dc)| if pipe_dir(grid[(rS + *dr) as usize][(cS + *dc) as usize]).contains(&(-dr, -dc)) {Some((*dr, *dc))} else {None})
        .collect();

    assert!(S_dirs.len() == 2);

    let mut cur1 = (rS, cS);
    let mut dir1 = S_dirs[0];
    let mut cur2 = (rS, cS);
    let mut dir2 = S_dirs[1];
    let mut dist = 0;

    let mut loop_r1: Vec<i32> = vec![rS];
    let mut loop_r2: Vec<i32> = vec![rS];
    let mut loop_c1: Vec<i32> = vec![cS];
    let mut loop_c2: Vec<i32> = vec![cS];
    let mut painted: HashSet<(i32, i32)> = HashSet::new();

    while (cur1.0 - cur2.0).abs() + (cur1.1 - cur2.1).abs() > 0 || dist < 5 {
        (cur1, dir1) = step(&cur1, &dir1, &grid, &mut loop_r1, &mut loop_c1, &mut painted, false); // get the sign from guess-and-check
        (cur2, dir2) = step(&cur2, &dir2, &grid, &mut loop_r2, &mut loop_c2, &mut painted, true);
        dist += 1;
    }
    dbg!(dist);

    let mut grid_sel: Vec<Vec<char>> = vec![vec!['.'; nc]; nr];
    for (r, c) in painted {
        grid_sel[r as usize][c as usize] = 'O';
    }

    for (r, c) in zip(loop_r1, loop_c1) {
        grid_sel[r as usize][c as usize] = grid[r as usize][c as usize];
    }
    for (r, c) in zip(loop_r2, loop_c2) {
        grid_sel[r as usize][c as usize] = grid[r as usize][c as usize];
    }

    flood_fill(&mut grid_sel, '.', 'O');

    // for char_vec in &grid_sel {   // draws the loop with the interior filled
    //     println!("{}", char_vec.iter().collect::<String>());
    // }

    let total: usize = (&grid_sel).iter().map(|v| v.iter().filter(|&&c| c == 'O').count()).sum();
    dbg!(total);


    Ok(())
}

pub fn step(cur: &(i32, i32), dir: &(i32, i32), grid: &Vec<Vec<char>>, r_vec: &mut Vec<i32>, c_vec: &mut Vec<i32>,
    paint: &mut HashSet<(i32, i32)>, sign: bool) -> ((i32, i32), (i32, i32)) {
    let rn = cur.0 + dir.0;
    let cn = cur.1 + dir.1;
    r_vec.push(rn);
    c_vec.push(cn);
    
    let next = (rn, cn);
    let next_char_dirs = pipe_dir(grid[rn as usize][cn as usize]);
    assert!(next_char_dirs.len() == 2);

    let next_dir = if next_char_dirs[0] == negative(&dir) {
        next_char_dirs[1]
    } else {next_char_dirs[0]};
    paint.insert(add(&next, &rot90(dir, sign)));
    paint.insert(add(&next, &rot90(&next_dir, sign)));

    (next, next_dir)
}

pub fn negative(a: &(i32, i32)) -> (i32, i32) {
    (-a.0, -a.1)
}

pub fn add(a: &(i32, i32), b: &(i32, i32)) -> (i32, i32) {
    (a.0 + b.0, a.1 + b.1)
}

pub fn rot90(&(x, y): &(i32, i32), sign: bool) -> (i32, i32) {
    if sign {(-y, x)} else {(y, -x)}
}

pub fn flood_fill(img: &mut Vec<Vec<char>>, from_c: char, to_c: char) {
    let mut frontier: BTreeSet<(i32, i32)> = BTreeSet::new();
    for r in 0..img.len() {
        for c in 0..img[0].len() {
            if img[r][c] == to_c {
                frontier.insert((r as i32, c as i32));
            }
        }
    }

    while frontier.len() > 0 {
        let (r, c) = frontier.pop_first().unwrap();
        for (dr, dc) in DIRS {
            let r2 = r+dr;
            let c2 = c+dc;
            if img[r2 as usize][c2 as usize] == from_c {
                img[r2 as usize][c2 as usize] = to_c;
                frontier.insert((r2, c2));
            }
        }
    }
}