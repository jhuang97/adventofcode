use std::collections::BTreeSet;
use std::fs;
use std::error::Error;
use std::i64;

#[derive(Eq, Hash, PartialEq, Copy, Clone, Debug)]
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

pub fn parse_dir(s: &str) -> Option<Direction> {
    match s {
        "U" => Some(Direction::N),
        "D" => Some(Direction::S),
        "R" => Some(Direction::E),
        "L" => Some(Direction::W),
        "3" => Some(Direction::N),
        "1" => Some(Direction::S),
        "0" => Some(Direction::E),
        "2" => Some(Direction::W),
        _ => None
    }
}

pub fn area(edges: &Vec<(Direction, i64)>) -> i64 {
    let mut inner2: i64 = 0;
    let mut edge2: i64 = 0;
    let mut r: i64 = 0;
    let mut c: i64 = 0;
    for (d, edge_len) in edges {
        let (dr, dc) = d.value();
        let r2 = r + dr as i64 * *edge_len;
        let c2 = c + dc as i64 * *edge_len;
        inner2 += (r + r2) * (c - c2);
        edge2 += *edge_len;

        r = r2;
        c = c2;
    }
    (inner2.abs() + edge2)/2 + 1
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input18.txt")?;
    // let input = fs::read_to_string("test18.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();

    let edges: Vec<(Direction, u32, String)> = lines.iter()
        .map(|s| {
            let (s1, s_c0) = s.split_once(" (#").unwrap();
            let (s_c, _) = s_c0.split_once(")").unwrap();
            let (s_d, s_l) = s1.split_once(" ").unwrap();
            (parse_dir(s_d).unwrap(), s_l.parse::<u32>().unwrap(), s_c.to_owned())
        }).collect();

    let edges1: Vec<(Direction, i64)> = (&edges).iter().map(|(d, l, _)| (*d, *l as i64)).collect();
    let edges2: Vec<(Direction, i64)> = (&edges).iter()
        .map(|(_, _, s)| {
            (parse_dir(&s[5..]).unwrap(), i64::from_str_radix(&s[..5], 16).unwrap())
        }).collect();

    dbg!(area(&edges1));
    dbg!(area(&edges2));

    // initial flood fill-based solution

    // let (mut r, mut c, mut r1, mut r2, mut c1, mut c2) = (0, 0, 0, 0, 0, 0);
    // for (d, edge_len, _) in &edges {
    //     let (dr, dc) = d.value();
    //     r += dr * *edge_len as i32;
    //     c += dc * *edge_len as i32;
    //     r1 = r1.min(r);
    //     c1 = c1.min(c);
    //     r2 = r2.max(r);
    //     c2 = c2.max(c);
    // }

    // let nr = (r2 - r1 + 1) as usize + 2;
    // let nc = (c2 - c1 + 1) as usize + 2;
    // let mut grid: Vec<Vec<u8>> = vec![vec![0; nc]; nr];

    // r = 1-r1;
    // c = 1-c1;
    // grid[r as usize][c as usize] = 1;
    // for (d, edge_len, _) in &edges {
    //     let (dr, dc) = d.value();
    //     for i in 1..=*edge_len {
    //         grid[(r + dr * i as i32) as usize][(c + dc * i as i32) as usize] = 1;
    //     }
    //     r += dr * *edge_len as i32;
    //     c += dc * *edge_len as i32;
    // }

    // for (dr, dc) in vec![(1, 1), (1, -1), (-1, 1), (-1, -1)] {
    //     let mut grid2 = grid.clone();
    //     flood_fill(&mut grid2, (dr-r1+1) as usize, (dc-c1+1) as usize, 0, 1);
    //     let count = grid2.iter().map(|v| v.iter().map(|n| *n as usize).sum::<usize>()).sum::<usize>();
    //     if !(grid2[0][0] == 1 && grid2[nr-1][0] == 1 && grid2[0][nc-1] == 1 && grid2[nr-1][nc-1] == 1) {
    //         dbg!(count);
    //     }
    // }

    Ok(())
}


static N: (i32, i32) = (-1, 0);
static S: (i32, i32) = (1, 0);
static E: (i32, i32) = (0, 1);
static W: (i32, i32) = (0, -1);
static DIRS: [(i32, i32); 4] = [N, E, S, W];

pub fn flood_fill(img: &mut Vec<Vec<u8>>, r0: usize, c0: usize, from_c: u8, to_c: u8) {
    let mut frontier: BTreeSet<(i32, i32)> = BTreeSet::new();
    frontier.insert((r0 as i32, c0 as i32));
    img[r0][c0] = to_c;
    let nr = img.len();
    let nc = img[0].len();

    while frontier.len() > 0 {
        let (r, c) = frontier.pop_first().unwrap();
        for (dr, dc) in DIRS {
            let r2 = r+dr;
            let c2 = c+dc;
            if 0 <= r2 && r2 < nr as i32 && 0 <= c2 && c2 < nc as i32 {
                if img[r2 as usize][c2 as usize] == from_c {
                    img[r2 as usize][c2 as usize] = to_c;
                    frontier.insert((r2, c2));
                }
            }
        }
    }
}