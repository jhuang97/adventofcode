use std::fs;
use std::error::Error;
use std::collections::HashMap;
use std::collections::HashSet;
use itertools::Itertools;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input08.txt")?;
    let (instr_str, network_str) = input.trim().split_once("\n\n").unwrap();

    let instr_left: Vec<bool> = instr_str.chars().map(|c| c == 'L').collect();
    let mut network: HashMap<String, (String, String)> = HashMap::new();
    let mut nodes_A: Vec<String> = Vec::new();
    // let mut nodes_Z: HashSet<String> = HashSet::new();

    for l in network_str.trim().lines() {
        match l.chars().nth(2).unwrap() {
            'A' => nodes_A.push(l[0..3].to_owned()),
            // 'Z' => nodes_Z.push(l[0..3].to_owned()),
            _ => (),
        };

        network.insert(l[0..3].to_owned(),
            (l[7..10].to_owned(),
            l[12..15].to_owned()));
    }

    let mut curr = "AAA";
    let mut i_idx = 0;
    let mut n_steps = 0;
    loop {
        let (left, right) = network.get(curr).unwrap();
        curr = if instr_left[i_idx] {left} else {right};
        n_steps += 1;

        if curr == "ZZZ" {
            break;
        }

        i_idx = (i_idx + 1) % instr_left.len();
    }

    dbg!(n_steps);

    let repeat_info = nodes_A.iter()
        .map(|n| get_z_repetition(n, &network, &instr_left))
        .collect_vec();

    for i in 0..(repeat_info.len()-1) {
        assert!(repeat_info[i].0 == repeat_info[i+1].0);
    }

    let mut n_steps_big: u64 = 1;
    for (_, _, t1, t2) in repeat_info {
        assert!(t1 * 2 == t2);
        n_steps_big = lcm(n_steps_big, t1 as u64);
    }
    dbg!(n_steps_big);

    Ok(())
}

pub fn get_z_repetition(start: &String, network: &HashMap<String, (String, String)>, instr_left: &Vec<bool>) -> (usize, String, i32, i32) {
    let mut z_hits: HashSet<(usize, String)> = HashSet::new();
    let mut i_idx = 0;
    let mut n_steps = 0;
    let mut curr = start.clone();
    let mut t1 = 0;
    let t2: i32;
    loop {
        let (left, right) = network.get(&curr).unwrap();
        curr = if instr_left[i_idx] {left.to_string()} else {right.to_string()};
        n_steps += 1;

        if curr.chars().nth(2).unwrap() == 'Z' {
            let state = (i_idx, curr.clone());
            if z_hits.contains(&state) {
                t2 = n_steps;
                break;
            } else {
                z_hits.insert(state);
                t1 = n_steps;
            }
        }

        i_idx = (i_idx + 1) % instr_left.len();
    }

    assert!(z_hits.len() == 1);
    let (i_idx, dest) = z_hits.iter().next().cloned().unwrap();

    (i_idx, dest, t1, t2)
}

pub fn gcd(a0: u64, b0: u64) -> u64 {
    let mut a = a0;
    let mut b = b0;
    while b != 0 {
        let t = b;
        b = a % b;
        a = t;
    }
    a
}

pub fn lcm(a: u64, b: u64) -> u64 {
    a * b / gcd(a, b)
}