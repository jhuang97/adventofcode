use std::collections::HashMap;
use std::fs;
use std::error::Error;

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

    fn opposite(&self) -> Direction {
        match *self {
            Direction::N => Direction::S,
            Direction::E => Direction::W,
            Direction::S => Direction::N,
            Direction::W => Direction::E,
        }
    }
}

pub fn parse_dir(c: char) -> Option<Direction> {
    match c {
        '^' => Some(Direction::N),
        'v' => Some(Direction::S),
        '>' => Some(Direction::E),
        '<' => Some(Direction::W),
        _ => None
    }
}

fn step(pt: (usize, usize), d: Direction) -> (usize, usize) {
    let (dr, dc) = d.value();
    let r2 = (pt.0 as i32 + dr) as usize;
    let c2 = (pt.1 as i32 + dc) as usize;
    (r2, c2)
}

const DIRS: [Direction; 4] = [Direction::N, Direction::E, Direction::S, Direction::W];

fn follow_trail(start: (usize, usize), dir0: Direction, grid: &Vec<Vec<char>>,
    branch_points: &HashMap<(usize, usize), Vec<Direction>>) -> ((usize, usize), usize, Direction) {

    let mut pt: (usize, usize) = step(start, dir0);
    let mut length: usize = 1;
    let mut dir = dir0;

    while !branch_points.contains_key(&pt) {
        let mut next_d_opt: Option<Direction> = None;
        for &d in &DIRS {
            if d != dir.opposite() {
                let (r2, c2) = step(pt, d);
                if grid[r2][c2] != '#' {
                    next_d_opt = Some(d);
                }
            }
        }
        length += 1;
        dir = next_d_opt.unwrap();
        pt = step(pt, dir);
    }
    
    (pt, length, dir)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input23.txt")?;
    // let input = fs::read_to_string("test23.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    let mut branch_points: HashMap<(usize, usize), Vec<Direction>> = HashMap::new();

    // identify branch points
    for r in 1..nr-1 {
        for c in 1..nc-1 {
            if grid[r][c] != '#' {
                let mut n_paths = 0;
                for d in DIRS {
                    let (r2, c2) = step((r, c), d);
                    if grid[r2][c2] != '#' {
                        n_paths += 1;
                    }
                }
                if n_paths > 2 {
                    branch_points.insert((r,c), Vec::new());
                }
            }
        }
    }
    // identify branch point exits
    for (pt, exits) in branch_points.iter_mut() {
        for &d in &DIRS {
            let (r2, c2) = step(*pt, d);
            if parse_dir(grid[r2][c2]).is_some_and(|d2| d2 == d) {
                exits.push(d);
            }
        }
    }
    let entrance = (0, 1);
    let exit = (nr-1, nc-2);
    // add entrance and exit so that follow_trail doesn't go out of bounds
    branch_points.insert(exit, Vec::new());
    branch_points.insert(entrance, Vec::new());

    let (branch_pt1, init_steps, _) = follow_trail(entrance, Direction::S, &grid, &branch_points);
    let mut trail_IDs: HashMap<((usize, usize), Direction), usize> = HashMap::new();
    let mut next_ID: usize = 1;

    let mut trails: HashMap<((usize, usize), Direction), ((usize, usize), usize, Direction)> = HashMap::new();
    for (pt, exits) in &branch_points {
        if *pt != entrance && *pt != exit {
            for d in &DIRS {
                let (r2, c2) = step(*pt, *d);
                if grid[r2][c2] != '#' { 
                    let (pt_o, trail_len, d_o) = follow_trail(*pt, *d, &grid, &branch_points);
                    let t_key = (*pt, *d);
                    let t_key_o = (pt_o, d_o.opposite());
                    if pt_o != entrance && !trail_IDs.contains_key(&t_key) && !trail_IDs.contains_key(&t_key_o) {
                        trail_IDs.insert(t_key, next_ID);
                        trails.insert(t_key, (pt_o, trail_len, d_o));

                        if pt_o != exit {
                            trail_IDs.insert(t_key_o, next_ID);
                            trails.insert(t_key_o, (*pt, trail_len, d.opposite()));
                        }

                        next_ID += 1;
                    }
                }
            }
        }
    }

    let most_steps = longest_hike(branch_pt1, init_steps, vec![],
        &branch_points, &trails, &exit).unwrap();
    dbg!(most_steps);

    let most_steps2 = longest_hike2(branch_pt1, init_steps, vec![], vec![branch_pt1],
        &grid, &trail_IDs, &trails, &exit).unwrap();
    dbg!(most_steps2);

    Ok(())
}


fn longest_hike(pt: (usize, usize), steps_so_far: usize, trails_so_far: Vec<((usize, usize), Direction)>,
    branch_points: &HashMap<(usize, usize), Vec<Direction>>,
    trails: &HashMap<((usize, usize), Direction), ((usize, usize), usize, Direction)>, end: &(usize, usize)) -> Option<usize> {

    if pt == *end {
        return Some(steps_so_far);
    }
    let mut most_steps: Option<usize> = None;
    for &exit_d in branch_points.get(&pt).unwrap() {
        let trail = (pt, exit_d);
        if !trails_so_far.contains(&trail) {
            let (pt2, new_steps, _) = trails.get(&trail).unwrap();
            let mut trails2 = trails_so_far.clone();
            trails2.push(trail);

            let steps_total = longest_hike(*pt2, steps_so_far + new_steps, trails2,
                branch_points, trails, end);
            most_steps = std::cmp::max(most_steps, steps_total);
        }
    }
    most_steps
}

fn longest_hike2(pt: (usize, usize), steps_so_far: usize, trail_IDs_so_far: Vec<usize>, points_so_far: Vec<(usize, usize)>,
    grid: &Vec<Vec<char>>, trail_IDs: &HashMap<((usize, usize), Direction), usize>,
    trails: &HashMap<((usize, usize), Direction), ((usize, usize), usize, Direction)>, end: &(usize, usize)) -> Option<usize> {

    if pt == *end {
        return Some(steps_so_far);
    }

    let mut most_steps: Option<usize> = None;
    for &d in &DIRS {
        let trail = (pt, d);
        if let Some(t_ID) = trail_IDs.get(&trail) {
            if !trail_IDs_so_far.contains(t_ID) {
                let (pt_o, new_steps, _) = trails.get(&trail).unwrap();
                if !points_so_far.contains(pt_o) {
                    let mut tID_new = trail_IDs_so_far.clone();
                    tID_new.push(*t_ID);
                    let mut pts_new = points_so_far.clone();
                    pts_new.push(*pt_o);

                    let steps_total = longest_hike2(*pt_o, steps_so_far + new_steps, 
                        tID_new, pts_new, grid, trail_IDs, trails, end);
                    // if points_so_far.len() < 5 && steps_total > most_steps {
                    //     dbg!(steps_total);
                    // }
                    most_steps = std::cmp::max(most_steps, steps_total);
                }
            }
        }
    }
    most_steps
}