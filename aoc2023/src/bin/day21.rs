use std::collections::{HashSet, HashMap};
use std::fs;
use std::error::Error;
use std::iter::zip;

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

const DIRS: [Direction; 4] = [Direction::N, Direction::E, Direction::S, Direction::W];

#[derive(Hash, Debug, Clone, Copy, Eq, PartialEq)]
struct Node {
    r: i32,
    c: i32,
}

fn dijkstra_to_multiple<F: Fn(&Node) -> Vec<(Node, i32)>>(start: Node, ends: &HashSet<Node>, 
    legal_moves: F) -> HashMap<Node, i32> {

    let mut m_ends = ends.clone();
    let mut dist: HashMap<Node, i32> = HashMap::new();
    let mut Q: Vec<Node> = vec![start];
    dist.insert(start, 0);
    let mut explored: HashSet<Node> = HashSet::new();

    while !Q.is_empty() {
        let mut min_dist = i32::MAX;
        let mut u = Q[0];
        for v in &Q {
            if dist[v] < min_dist {
                min_dist = dist[v];
                u = *v;
            }
        }
        Q.retain(|x| *x != u);

        if m_ends.contains(&u) {
            m_ends.remove(&u);
        }
        if ends.is_empty() {
            return dist;
        }
        explored.insert(u);
        for (v, cost) in legal_moves(&u) {
            let alt = dist[&u] + cost;
            if !explored.contains(&v) && !Q.contains(&v) {
                Q.push(v);
                dist.insert(v, alt);
            } else if Q.contains(&v) && alt < dist[&v] {
                dist.insert(v, alt);
            }
        }
    }

    dist
}

fn dijkstra_extend<F: Fn(&Node) -> Vec<(Node, i32)>>(start_dists: &HashMap<Node, i32>, ends: &HashSet<Node>, 
    legal_moves: F) -> HashMap<Node, i32> {

    let mut m_ends = ends.clone();
    let mut dist = start_dists.clone();
    let mut Q: Vec<Node> = dist.keys().into_iter().cloned().collect();
    let mut explored: HashSet<Node> = HashSet::new();

    while !Q.is_empty() {
        let mut min_dist = i32::MAX;
        let mut u = Q[0];
        for v in &Q {
            if dist[v] < min_dist {
                min_dist = dist[v];
                u = *v;
            }
        }
        Q.retain(|x| *x != u);

        if m_ends.contains(&u) {
            m_ends.remove(&u);
        }
        if ends.is_empty() {
            return dist;
        }
        explored.insert(u);
        for (v, cost) in legal_moves(&u) {
            let alt = dist[&u] + cost;
            if !explored.contains(&v) && !Q.contains(&v) {
                Q.push(v);
                dist.insert(v, alt);
            } else if Q.contains(&v) && alt < dist[&v] {
                dist.insert(v, alt);
            }
        }
    }

    dist
}

fn legal_moves(n: &Node, nr: i32, grid: &Vec<Vec<char>>) -> Vec<(Node, i32)> {
    let mut out = Vec::new();
    for d in &DIRS {
        let (dr, dc) = d.value();
        let r2 = n.r + dr;
        let c2 = n.c + dc;
        if 0 <= r2 && r2 < nr && 0 <= c2 && c2 < nr {
            if grid[r2 as usize][c2 as usize] != '#' {
                out.push((Node { r: r2, c: c2 }, 1));
            }
        }
    }
    out
}

fn dist_to_tile_border(rS: i32, cS: i32, grid: &Vec<Vec<char>>) -> HashMap<Node, i32> {
    let nr = grid.len();
    let nc = grid[0].len();
    let mut ends: HashSet<Node> = HashSet::new();
    for r in 0..nr {
        ends.insert(Node { r: r as i32, c: 0 });
        ends.insert(Node { r: r as i32, c: nc as i32 - 1 });
    }
    for c in 0..nc {
        ends.insert(Node { r: 0, c: c as i32 });
        ends.insert(Node { r: nr as i32 - 1, c: c as i32 });
    }

    dijkstra_to_multiple(Node { r: rS, c: cS }, &ends, 
        |n| legal_moves(n, nr as i32, grid))
}

fn n_reachable(rS: i32, cS: i32, n_steps: i32, grid: &Vec<Vec<char>>) -> usize {
    let nr = grid.len();
    let nc = grid[0].len();

    let mut all_nodes: HashSet<Node> = HashSet::new();
    for r in 0..nr as i32 { for c in 0..nc as i32 {
        all_nodes.insert(Node {r, c});
    }}

    let dists = dijkstra_to_multiple(Node { r: rS, c: cS }, &all_nodes, 
        |n| legal_moves(n, nr as i32, grid));

    dists.values().filter(|&&d| d <= n_steps && (d-n_steps) % 2 == 0).count()
}

fn propagate_straight(propagation_dir: Direction, n_steps: i32, 
    grid: &Vec<Vec<char>>, border_dists: &HashMap<Node, i32>) -> (usize, usize, usize) {

    let nr = grid.len();
    let nc = grid[0].len();

    let start_pos: i32 = match propagation_dir {
        Direction::E | Direction::S => -1,
        Direction::W | Direction::N => nr as i32,
    };
    
    let end_pos: i32 = match propagation_dir {
        Direction::E | Direction::S => nr as i32 - 1,
        Direction::W | Direction::N => 0,
    };

    let start_nodes: Vec<Node> = match propagation_dir {
        Direction::N | Direction::S => (0..nc as i32)
            .map(|c| Node {r: start_pos, c}).collect(),
        Direction::E | Direction::W => (0..nr as i32)
            .map(|r| Node {r, c: start_pos}).collect(),
    };

    let end_nodes: Vec<Node> = match propagation_dir {
        Direction::N | Direction::S => (0..nc as i32)
            .map(|c| Node {r: end_pos, c}).collect(),
        Direction::E | Direction::W => (0..nr as i32)
            .map(|r| Node {r, c: end_pos}).collect(),
    };

    let end_set: HashSet<Node> = HashSet::from_iter(end_nodes.iter().cloned());

    let mut all_nodes: HashSet<Node> = HashSet::new();
    for r in 0..nr as i32 { for c in 0..nc as i32 {
        all_nodes.insert(Node {r, c});
    }}

    let min_dist_from_side = nr as i32;
    let max_dist_from_side = max_dist_from_side(propagation_dir, grid);
    let mut dists: Vec<i32> = (&end_nodes).iter().map(|n| *border_dists.get(&n).unwrap()).collect();
    let mut steps_left = n_steps;
    let mut n_tiles = 0;
    let mut n_tiles_odd = 0;
    let mut n_tiles_even = 0;
    let mut n_plots = 0;

    let mut dist_memo: HashMap<Vec<i32>, Vec<i32>> = HashMap::new();

    loop {
        let min_dist = *(&dists).iter().min().unwrap();
        if steps_left <= min_dist {
            break;
        }
        for v in dists.iter_mut() {
            *v -= min_dist;
        }
        steps_left -= min_dist;

        if steps_left < max_dist_from_side {
            // not all possible plots in tile reached
            let start_dists: HashMap<Node, i32> = zip(start_nodes.iter().cloned(), dists).collect();
            let dist_map = dijkstra_extend(&start_dists, 
                &all_nodes, 
                |n| legal_moves(n, nr as i32, grid));
            for (n, dist) in &dist_map {
                if *dist <= steps_left && (*dist - steps_left) % 2 == 0 {
                    if 0 <= n.r && n.r < nr as i32 && 0 <= n.c && n.c < nc as i32 {
                        n_plots += 1;
                    }
                }
            }
            if steps_left <= min_dist_from_side {
                break;
            }
            n_tiles += 1;
            dists = (&end_nodes).iter().map(|n| *dist_map.get(&n).unwrap()).collect();
        } else {
            // all plots of the correct parity in this tile will be reached
            dists = if !dist_memo.contains_key(&dists) {
                let start_dists: HashMap<Node, i32> = zip(start_nodes.iter().cloned(), dists.clone()).collect();
                let dist_map = dijkstra_extend(&start_dists, 
                    &end_set, 
                    |n| legal_moves(n, nr as i32, grid));
                let dist_new: Vec<_> = (&end_nodes).iter().map(|n| *dist_map.get(&n).unwrap()).collect();
                dist_memo.insert(dists, dist_new.clone());
                dist_new
            } else {
                dist_memo.get(&dists).unwrap().clone()
            };
            n_tiles += 1;
            if (n_steps + n_tiles) % 2 == 0 {
                n_tiles_even += 1;
            } else {
                n_tiles_odd += 1;
            }
        }
    }

    (n_tiles_even, n_tiles_odd, n_plots)
}

fn propagate_diagonal(propagation_dir: Direction, n_steps: i32, 
    grid: &Vec<Vec<char>>, border_dists: &HashMap<Node, i32>) -> (usize, usize, usize) {

    let nr = grid.len();
    let nc = grid[0].len();

    // E -> SE, S -> SW, W -> NW, N -> NE
    let end_r = match propagation_dir {
        Direction::E | Direction::S => nr as i32 - 1,
        Direction::N | Direction::W => 0,
    };
    let end_c = match propagation_dir {
        Direction::E | Direction::N => nc as i32 - 1,
        Direction::S | Direction::W => 0,
    };
    let start_r = (nr as i32 - 1) - end_r;
    let start_c = (nc as i32 - 1) - end_c;

    let start_pt = Node { r: start_r, c: start_c };
    let end_pt = Node { r: end_r, c: end_c };

    let mut all_nodes: HashSet<Node> = HashSet::new();
    for r in 0..nr as i32 { for c in 0..nc as i32 {
        all_nodes.insert(Node {r, c});
    }}
    let max_dist_from_corner = *dijkstra_to_multiple(start_pt, &all_nodes,
        |n| legal_moves(n, nr as i32, grid)).values().max().unwrap();

    let mut steps_left = n_steps - border_dists.get(&end_pt).unwrap() - 2;
    let mut n_tiles: usize = 1;
    let mut n_tiles_odd = 0;
    let mut n_tiles_even = 0;
    let mut n_plots = 0;

    loop {
        if steps_left < max_dist_from_corner {
            // not all possible plots in tile reached
            let dists = dijkstra_to_multiple(start_pt, &all_nodes,
                |n| legal_moves(n, nr as i32, grid));
            for &dist in dists.values() {
                if dist <= steps_left && (dist - steps_left) % 2 == 0 {
                    n_plots += n_tiles;
                }
            }

            if steps_left < nr as i32 {
                break;
            }
        } else {
            // all possible plots in tile reached
            if (n_steps + n_tiles as i32 + 1) % 2 == 0 {
                n_tiles_even += n_tiles;
            } else {
                n_tiles_odd += n_tiles;
            }
        }
        n_tiles += 1;
        steps_left -= nr as i32;
    }

    (n_tiles_even, n_tiles_odd, n_plots)
}

fn max_dist_from_side(propagation_dir: Direction, grid: &Vec<Vec<char>>) -> i32 {
    let nr = grid.len();
    let nc = grid[0].len();
    let start_pos: i32 = match propagation_dir {
        Direction::E | Direction::S => -1,
        Direction::W | Direction::N => nr as i32,
    };
    let start_dists: HashMap<Node, i32> = match propagation_dir {
        Direction::N | Direction::S => (0..nc as i32)
            .map(|c| (Node {r: start_pos, c}, 0)).collect(),
        Direction::E | Direction::W => (0..nr as i32)
            .map(|r| (Node { r, c: start_pos }, 0)).collect(),
    };
    let mut ends: HashSet<Node> = HashSet::new();
    for r in 0..nr as i32 { for c in 0..nc as i32 {
        ends.insert(Node {r, c});
    }}
    
    let dists = dijkstra_extend(&start_dists, &ends,
        |n| legal_moves(n, nr as i32, grid));

    dists.into_values().max().unwrap()
}

fn n_plots_by_parity(rS: i32, cS: i32, grid: &Vec<Vec<char>>) -> [usize; 2] {
    let nr = grid.len();
    let nc = grid[0].len();
    let mut ends: HashSet<Node> = HashSet::new();
    for r in 0..nr as i32 { for c in 0..nc as i32 {
        ends.insert(Node {r, c});
    }}

    let dists = dijkstra_to_multiple(Node { r: rS, c: cS }, &ends,
        |n| legal_moves(n, nr as i32, grid));

    let mut out = [0, 0];
    for d in dists.values() {
        out[(d % 2) as usize] += 1;
    }
    out
}

fn n_reachable2(n_steps2: i32, rS: usize, cS: usize, grid: &Vec<Vec<char>>, border_dists: &HashMap<Node, i32>) -> usize {
    let mut n_left_all = 0;
    let mut n_even_all = 0;
    let mut n_odd_all = 0;

    for &d in &DIRS {
        let (n_even, n_odd, n_left) = propagate_diagonal(d, n_steps2, &grid, &border_dists);
        n_even_all += n_even;
        n_odd_all += n_odd;
        n_left_all += n_left;
        let (n_even, n_odd, n_left) = propagate_straight(d, n_steps2, &grid, &border_dists);
        n_even_all += n_even;
        n_odd_all += n_odd;
        n_left_all += n_left;
    }

    let n_parity = n_plots_by_parity(rS as i32, cS as i32, &grid);

    n_reachable(rS as i32, cS as i32, n_steps2, &grid) +
        n_even_all * n_parity[0] + n_odd_all * n_parity[1] + n_left_all
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input21.txt")?; let n_steps1: i32 = 64;
    // let input = fs::read_to_string("test21.txt")?; let n_steps1: i32 = 6;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let grid: Vec<Vec<char>> = lines.iter().map(|x| x.chars().collect()).collect();
    let nr = grid.len();
    let nc = grid[0].len();

    assert!(nr == nc);

    let (mut rS, mut cS) = (0, 0);
    for r in 0..nr {
        for c in 0..nc {
            if grid[r][c] == 'S' {
                rS = r;
                cS = c;
            }
        }
    }

    // original part 1 solution

    // let mut reachable: HashSet<(i32, i32)> = HashSet::from([(rS as i32, cS as i32)]);
    // for i in 0..n_steps1 {
    //     let mut r_next: HashSet<(i32, i32)> = HashSet::new();
    //     for (r, c) in reachable.drain() {
    //         for d in &DIRS {
    //             let (dr, dc) = d.value();
    //             let r2 = r + dr;
    //             let c2 = c + dc;
    //             if 0 <= r2 && r2 < nr as i32 && 0 <= c2 && c2 < nc as i32 {
    //                 if grid[r2 as usize][c2 as usize] != '#' {
    //                     r_next.insert((r2, c2));
    //                 }
    //             }
    //         }
    //     }
    //     reachable.extend(&r_next);
    // }
    // dbg!(reachable.len());

    let n_plots1 = n_reachable(rS as i32, cS as i32, n_steps1, &grid);
    dbg!(n_plots1);

    let border_dists = dist_to_tile_border(rS as i32, cS as i32, &grid);

    let n_plots2 = n_reachable2(26501365, rS, cS, &grid, &border_dists);
    dbg!(n_plots2);

    // for n_steps2 in [6, 10, 50, 100, 500, 1000, 5000] { // gives a value that is slightly different than the website's value for 500 steps
    //     let n_plots2 = n_reachable2(n_steps2, rS, cS, &grid, &border_dists);
    //     println!("{n_steps2} steps, {n_plots2} plots");
    // }

    Ok(())
}