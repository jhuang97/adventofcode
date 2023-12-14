use std::fs;
use std::error::Error;


pub fn rot(grid: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let nr = grid.len();
    let mut rot_grid: Vec<Vec<char>> = vec![vec!['.'; nr]; nr];

    for r in 0..nr {
        for c in 0..nr {
            rot_grid[c][nr-r-1] = grid[r][c];
        }
    }
    rot_grid
}


pub fn tilt_north(grid: &Vec<Vec<char>>) -> Vec<Vec<char>> {
    let nr = grid.len();
    let mut tilted_grid: Vec<Vec<char>> = vec![vec!['.'; nr]; nr];

    for r in 0..nr {
        for c in 0..nr {
            if grid[r][c] == '#' {
                tilted_grid[r][c] = '#';
            }
        }
    }

    for c in 0..nr {
        let mut r_catch: i32 = -1;
        let mut r = 0;
        let mut n_rocks = 0;
        while r < nr {
            match grid[r][c] {
                'O' => n_rocks += 1,
                '#' => {
                    if n_rocks > 0 {
                        for dr in 0..n_rocks {
                            tilted_grid[(r_catch+dr+1) as usize][c] = 'O';
                        }
                        n_rocks = 0;
                    }
                    r_catch = r as i32;
                },
                _ => (),
            }
            r += 1;
        }
        if n_rocks > 0 {
            for dr in 0..n_rocks {
                tilted_grid[(r_catch+dr+1) as usize][c] = 'O';
            }
            n_rocks = 0;
        }
    }

    tilted_grid
}

pub fn spin_cycle(grid: &mut Vec<Vec<char>>) {
    for _ in 0..4 {
        *grid = tilt_north(grid);
        *grid = rot(&grid);
    }
}

pub fn total_load(grid: &Vec<Vec<char>>) -> i32 {
    let mut total = 0;
    for r in 0..grid.len() {
        for c in 0..grid.len() {
            if grid[r][c] == 'O' {
                total += grid.len() as i32 - r as i32;
            }
        }
    }
    total
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input14.txt")?;
    // let input = fs::read_to_string("test14.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    assert!(nr == nc);

    let tilted_grid: Vec<Vec<char>> = tilt_north(&grid);
    let load1 = total_load(&tilted_grid);
    
    dbg!(load1);

    let mut grid2 = grid.clone();
    let mut history: Vec<Vec<Vec<char>>> = vec![grid2.clone()];
    let mut n = 0;
    loop {
        spin_cycle(&mut grid2);
        n += 1;
        if !history.contains(&grid2) {
            history.push(grid2.clone());
        } else {
            break;
        }
    }
    let n0 = (&history).iter().position(|s| *s == grid2).unwrap();
    let period = n - n0;
    let n_match = (1000000000 - n0) % period + n0;
    let grid_match = &history[n_match];
    let load2: i32 = total_load(grid_match);
    dbg!(load2);

    Ok(())
}


pub fn print_grid(grid: &Vec<Vec<char>>) {
    for v in grid {
        for c in v {
            print!("{}", c);
        }
        println!();
    }
}

pub fn encode_state(grid: &Vec<Vec<char>>) -> Vec<u8> {
    let mut v = Vec::new();
    for r in 0..grid.len() {
        for c in 0..grid.len() {
            if grid[r][c] == 'O' {
                v.push(r as u8);
                v.push(c as u8);
            }
        }
    }
    v
}
