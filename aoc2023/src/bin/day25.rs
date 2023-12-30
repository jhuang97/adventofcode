use std::collections::{HashSet, HashMap};
use std::fs;
use std::error::Error;
use rand::prelude::*;


fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input25.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let info: Vec<(&str, Vec<&str>)> = lines.iter().map(|s| {
        let (s1, s2) = s.split_once(": ").unwrap();
        (s1, s2.split(" ").collect())
    }).collect();

    let mut graph: HashMap<&str, HashSet<&str>> = HashMap::new();
    for (n1, nodes) in &info {
        for n in nodes {
            (*graph.entry(*n1).or_insert(HashSet::new())).insert(n);
            (*graph.entry(*n).or_insert(HashSet::new())).insert(n1);
        }
    }
    // dbg!(graph.len());

    // let mut degree_distr: HashMap<usize, usize> = HashMap::new();
    // for neighbors in graph.values() {
    //     *(degree_distr.entry(neighbors.len()).or_insert(0)) += 1;
    // }
    // dbg!(&degree_distr);

    let mut team: HashMap<&str, bool> = HashMap::new();
    for n in graph.keys() {
        team.insert(n, random());
    }

    for i in 0..50 {
        for (n, neighbors) in &graph {
            let mut n_true = 0;
            let mut n_false = 0;
            for nb in neighbors {
                if team[nb] { n_true += 1; } else { n_false += 1; }
            }

            let neighbor_team = if n_true > n_false {
                true
            } else if n_false > n_true {
                false
            } else {
                random()
            };

            team.insert(n, neighbor_team);
        }

        let mut bad_edges = 0;
        for (n, neighbors) in &graph {
            for nb in neighbors {
                if team[n] != team[nb] {
                    bad_edges += 1;
                }
            }
        }

        if bad_edges <= 6 {
            // println!("{i} iterations needed");
            break;
        }
    }

    let mut n_true = 0;
    let mut n_false = 0;
    for &v in team.values() {
        if v { n_true += 1; } else { n_false += 1; }
    }
    let prod = n_true * n_false;
    dbg!(prod);

    Ok(())
}