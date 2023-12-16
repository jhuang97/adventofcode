use std::collections::HashSet;
use std::fs;
use std::error::Error;

#[derive(Eq, Hash, PartialEq, Copy, Clone)]
pub enum Direction {
    N, E, S, W
}

impl Direction {
    fn value(&self) -> (i32, i32) {  // (row, column)
        match *self {
            Direction::N => (-1, 0),
            Direction::E => (0, 1),
            Direction::S => (1, 0),
            Direction::W => (0, -1),
        }
    }
}

pub fn encounter(d0: Direction, c: char) -> Vec<Direction> {
    match c {
        '.' => vec![d0],
        '/' => vec![match d0 {
            Direction::N => Direction::E,
            Direction::E => Direction::N,
            Direction::S => Direction::W,
            Direction::W => Direction::S,
        }],
        '\\' => vec![match d0 {
            Direction::N => Direction::W,
            Direction::W => Direction::N,
            Direction::S => Direction::E,
            Direction::E => Direction::S,
        }],
        '|' => match d0 {
            Direction::N | Direction::S => vec![d0],
            Direction::E | Direction::W => vec![Direction::N, Direction::S],
        },
        '-' => match d0 {
            Direction::E | Direction::W => vec![d0],
            Direction::N | Direction::S => vec![Direction::E, Direction::W],
        },
        _ => unreachable!()
    }
}

pub fn n_energized(grid: &Vec<Vec<char>>, init: (i32, i32, Direction)) -> usize {
    let nr = grid.len();
    let nc = grid[0].len();

    let mut light: Vec<Vec<HashSet<Direction>>> = Vec::new();
    for i in 0..nr {
        light.push(Vec::new());
        for _ in 0..nc {
            light[i].push(HashSet::new());
        }
    }

    let mut propagating: Vec<(i32, i32, Direction)> = vec![init];
    while propagating.len() > 0 {
        let (r, c, dir) = propagating.pop().unwrap();
        light[r as usize][c as usize].insert(dir);
        for d_new in encounter(dir, grid[r as usize][c as usize]) {
            let (dr, dc) = d_new.value();
            let r2 = r + dr;
            let c2 = c + dc;
            if 0 <= r2 && r2 < nr as i32 && 0 <= c2 && c2 < nc as i32 {
                if !light[r2 as usize][c2 as usize].contains(&d_new) {
                    propagating.push((r2, c2, d_new));
                }
            }
        }
    }

    let total = light.iter()
        .map(|v| v.iter()
                .map(|c| (c.len() > 0) as usize)
                .sum::<usize>())
        .sum::<usize>();
    total
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input16.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    let total = n_energized(&grid, (0, 0, Direction::E));
    dbg!(total);

    let mut best_total = total;
    for c in 0..nc {
        best_total = best_total.max(n_energized(&grid, (0, c as i32, Direction::S)));
        best_total = best_total.max(n_energized(&grid, (nr as i32 - 1, c as i32, Direction::N)));
    }

    for r in 0..nr {
        best_total = best_total.max(n_energized(&grid, (r as i32, 0, Direction::E)));
        best_total = best_total.max(n_energized(&grid, (r as i32, nc as i32 - 1, Direction::W)));
    }
    dbg!(best_total);

    Ok(())
}