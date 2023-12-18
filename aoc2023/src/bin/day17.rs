use std::fs;
use std::error::Error;
use std::cmp::Ordering;
use std::collections::HashMap;
use std::collections::BinaryHeap;


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

#[derive(Eq, Hash, PartialEq, Copy, Clone, Debug)]
pub struct Node {
    r: usize,
    c: usize,
    streak: usize,
    dir: Direction,    
}

impl Ord for Node {
    fn cmp(&self, other: &Self) -> Ordering {
        self.r.cmp(&other.r)
            .then_with(|| self.c.cmp(&other.c))
    }
}

impl PartialOrd for Node {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

#[derive(Copy, Clone, Eq, PartialEq)]
struct State {
    cost: u32,
    position: Node,
}

impl Ord for State {
    fn cmp(&self, other: &Self) -> Ordering {
        // std::collections::binaryheap is a max-heap by default; hence reverse the comparator here
        other.cost.cmp(&self.cost)
            .then_with(|| self.position.cmp(&other.position))
    }
}

impl PartialOrd for State {
    fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
        Some(self.cmp(other))
    }
}

pub struct AStarSolver {
    nr: usize,
    nc: usize,
    grid: Vec<Vec<u32>>,
}

impl AStarSolver {
    pub fn a_star_3blocks(&self, start: &Node, is_ultra: bool) -> u32 {
        // let mut came_from: HashMap<Node, Node> = HashMap::new();
        let mut g_score: HashMap<Node, u32> = HashMap::new();
        g_score.insert(*start, 0);
        let mut f_score: HashMap<Node, u32> = HashMap::new();
        f_score.insert(*start, self.heuristic_to_end(start));
        let mut Q = BinaryHeap::new();
        Q.push(State {cost: *f_score.get(start).unwrap(), position: *start });

        // let mut goal_dists: HashMap<Node, u32> = HashMap::new();

        while let Some(State { cost, position: curr }) = Q.pop() {
            if self.is_goal(&curr) {
                return *g_score.get(&curr).unwrap();

                // Technically in this setup, we are not navigating to one node but to multiple nodes,
                // each with the same row and column but different values of streak and position, so it's not 
                // obvious to me that the first goal node that is reached by the algorithm is the closest.
                // That's why earlier I was computing distance to all the goal nodes.

                // println!("{}", *g_score.get(&curr).unwrap());
                // goal_dists.insert(curr, *g_score.get(&curr).unwrap());
                // if self.is_complete(&goal_dists, is_ultra) {
                //     return goal_dists;
                // }
            }

            for v in if is_ultra {self.legal_moves_ultra(&curr)} else {self.legal_moves(&curr)} {
                let tentative_g = g_score.get(&curr).unwrap() + self.length(&curr, &v);
                if tentative_g < *g_score.get(&v).unwrap_or(&u32::MAX) {
                    g_score.insert(v, tentative_g);
                    f_score.insert(v, tentative_g + self.heuristic_to_end(&v));
                    Q.push(State {cost: *f_score.get(&v).unwrap(), position: v});
                }
            }
        }
        unreachable!()
        // goal_dists
    }

    pub fn is_goal(&self, n: &Node) -> bool {
        n.r == self.nr-1 && n.c == self.nc - 1
    }

    pub fn length(&self, from: &Node, to: &Node) -> u32 {
        self.grid[to.r][to.c]
    }

    pub fn out_of_bounds(&self, r: i32, c: i32) -> bool {
        r < 0 || r >= self.nr as i32 || c < 0 || c >= self.nc as i32
    }

    pub fn legal_moves_ultra(&self, n: &Node) -> Vec<Node> {
        let mut out = Vec::new();
        for d in if n.streak == 0 { vec![Direction::E, Direction::S] }
            else if n.streak < 4 {vec![n.dir]}
            else { vec![Direction::N, Direction::E, Direction::W, Direction::S] }  
        {
            if n.dir.opposite() != d && !(n.streak >= 10 && d == n.dir) {
                let (dr, dc) = d.value();
                let r2 = n.r as i32 + dr;
                let c2 = n.c as i32 + dc;
                let will_crash = d != n.dir && self.out_of_bounds(n.r as i32 + 4*dr, n.c as i32 + 4*dc);

                if !will_crash && !self.out_of_bounds(r2, c2) {
                    out.push(Node {
                        r: r2 as usize,
                        c: c2 as usize,
                        streak: if d == n.dir { n.streak + 1 } else { 1 },
                        dir: d
                    })
                }
            }
        }

        out
    }

    pub fn legal_moves(&self, n: &Node) -> Vec<Node> {
        let mut out = Vec::new();
        for d in &[Direction::N, Direction::E, Direction::W, Direction::S] {
            if n.dir.opposite() != *d && !(n.streak >= 3 && *d == n.dir) {
                let (dr, dc) = d.value();
                let r2 = n.r as i32 + dr;
                let c2 = n.c as i32 + dc;
                if !self.out_of_bounds(r2, c2) {
                    out.push(Node {
                        r: r2 as usize,
                        c: c2 as usize,
                        streak: if *d == n.dir { n.streak + 1 } else { 1 },
                        dir: *d
                    })
                }
            }
        }

        out
    }

    pub fn heuristic_to_end(&self, n: &Node) -> u32 {
        (self.nr-1 - n.r + self.nc-1 - n.c) as u32
    }

    pub fn is_complete(&self, dists: &HashMap<Node, u32>, is_ultra: bool) -> bool {
        if is_ultra {
            for k in 1..self.nc {
                if !dists.contains_key(&Node {r: self.nr-1, c: self.nc-1, streak: k as usize, dir: Direction::E}) {
                    return false;
                }
            }
            for k in 1..self.nr {
                if !dists.contains_key(&Node {r: self.nr-1, c: self.nc-1, streak: k as usize, dir: Direction::S}) {
                    return false;
                }
            }
            true
        } else {
            for k in 1..=3 {
                if !dists.contains_key(&Node {r: self.nr-1, c: self.nc-1, streak: k as usize, dir: Direction::E}) {
                    return false;
                }
                if !dists.contains_key(&Node {r: self.nr-1, c: self.nc-1, streak: k as usize, dir: Direction::S}) {
                    return false;
                }
            }
            true
        }
    }
}


fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input17.txt")?;
    // let input = fs::read_to_string("test17.txt")?;
    // let input = fs::read_to_string("test17_2.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<u32>> = lines.iter().map(|x| x.chars().map(|c| c.to_digit(10).unwrap()).collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    let solver = AStarSolver { nr, nc, grid };
    let dist = solver.a_star_3blocks(&Node { r: 0, c: 0, streak: 0, dir: Direction::E }, false);
    dbg!(dist);

    let dist2 = solver.a_star_3blocks(&Node { r: 0, c: 0, streak: 0, dir: Direction::E }, true);
    dbg!(dist2);

    Ok(())
}