use std::fs;
use std::error::Error;
use itertools::Itertools;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input12.txt")?;
    // let input = fs::read_to_string("test12.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();
    let parse_fn = |s: &&str| {
        let (spring_str, num_str) = s.split_once(" ").unwrap();
        let num_vec: Vec<usize> = num_str.split(",").map(|n| n.parse().unwrap()).collect();
        (spring_str.chars().collect(), num_vec)
    };
    let records: Vec<(Vec<char>, Vec<usize>)> = lines.iter()
        .map(parse_fn).collect();

    let mut total = 0;
    for (i, r) in (&records).iter().enumerate() {
        // dbg!(i);
        total += attempt_solve(r, false);
    }
    dbg!(total);

    let mut total2 = 0;
    for (i, r) in (&records).iter().enumerate() {
        // dbg!(i);
        total2 += attempt_solve(r, true);
    }
    dbg!(total2);

    Ok(())
}

pub fn dbg_state((springs, group_sizes): &(Vec<char>, Vec<usize>)) {
    let spring_str: String = springs.iter().collect();
    println!("'{}' {}", spring_str, group_sizes.iter().format(","));
}

pub fn attempt_solve((springs, group_sizes): &(Vec<char>, Vec<usize>), big: bool) -> u64 {
    let mut state = if big {
        let mut big_springs = springs.clone();
        for _ in 0..4 {
            big_springs.push('?');
            big_springs.append(&mut springs.clone());
        }
        (big_springs,
        group_sizes.iter().cloned().cycle().take(group_sizes.len() * 5).collect::<Vec<_>>())
    } else {
        (springs.clone(), group_sizes.clone())
    };

    state = reduce_from_ends(&state);
    let ans1 = n_ways(&state);

    ans1
}

pub fn n_ways(state: &(Vec<char>, Vec<usize>)) -> u64 {
    match state.1.len() {
        0 => if state.0.contains(&'#') { 0 } else { 1 },
        1 => n_ways_naive(state),
        _ => if state.0.contains(&'.') { n_ways_split_op(state) } // split at '.'
            else {
                n_ways_split_dq(state) // split at '#' or '?'
            }
    }
}

pub fn n_ways_split_dq((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> u64 {
    let split_idx = springs.len() / 2;
    let mut total = 0;

    if springs[split_idx] != '#' {
        let springs_left = springs[..split_idx].to_vec();
        let springs_right = springs[split_idx+1..].to_vec();
        let ndq_left = springs_left.iter().filter(|c| **c != '.').count() as i32;
        let ndq_right = springs_right.iter().filter(|c| **c != '.').count() as i32;
        total += n_ways_clean_split(springs_left, springs_right, group_sizes, ndq_left, ndq_right);
    }

    total += n_ways_messy_split(springs, group_sizes, split_idx);
    total
}

pub fn n_ways_messy_split(springs: &Vec<char>, group_sizes: &Vec<usize>, split_idx: usize) -> u64 {
    let mut total = 0;

    // there might actually be fewer '#' or '?' on either side after the split because some 
    // will be consumed by the spring group in the middle
    let ndq_left = springs[..split_idx].iter().filter(|c| **c != '.').count();
    let ndq_right = springs[split_idx+1..].iter().filter(|c| **c != '.').count();

    for g_split in 0..group_sizes.len() {
        let ng_left = group_sizes[..g_split].iter().sum::<usize>();
        let ng_right = group_sizes[g_split+1..].iter().sum::<usize>();
        if ng_left <= ndq_left && ng_right <= ndq_right {
            let gmid = group_sizes[g_split];
            let igmid_min = if split_idx + 1 < gmid { 0 } else { split_idx + 1 - gmid };
            for igmid in igmid_min..=split_idx {
                if possible_mid(springs, igmid, gmid, ng_left, ng_right) {
                    if messy_left_ok(springs, igmid, ng_left) && messy_right_ok(springs, igmid+gmid, ng_right) {
                        let subtotal = if ng_left == 0 { 1 } else { n_ways(&(springs[..igmid-1].to_vec(), group_sizes[..g_split].to_vec())) }
                            * if ng_right == 0 { 1 } else { n_ways(&(springs[igmid+gmid+1..].to_vec(), group_sizes[g_split+1..].to_vec())) };
                        total += subtotal;
                    }
                }
            }
        }
    }

    total
}

pub fn messy_left_ok(springs: &Vec<char>, i_right: usize, ng: usize) -> bool {
    if ng == 0 {
        return !springs[..i_right].contains(&'#');
    }
    if i_right < 2 {
        return false;
    }
    let sub_str = springs[..i_right-1].to_vec();
    let ndq = sub_str.iter().filter(|c| **c != '.').count();
    let nd = sub_str.iter().filter(|c| **c == '#').count();
    nd <= ng && ng <= ndq
}

pub fn messy_right_ok(springs: &Vec<char>, i_left: usize, ng: usize) -> bool {
    if ng == 0 {
        return !springs[i_left..].contains(&'#');
    }
    if i_left + 1 >= springs.len() {
        return false;
    }
    let sub_str = springs[i_left+1..].to_vec();
    let ndq = sub_str.iter().filter(|c| **c != '.').count();
    let nd = sub_str.iter().filter(|c| **c == '#').count();
    nd <= ng && ng <= ndq
}

pub fn n_ways_split_op((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> u64 {
    // first figure out the best '.' to split on
    let op_indices: Vec<usize> = springs.iter().enumerate()
        .filter_map(|(i, c)| if *c == '.' {Some(i)} else {None})
        .collect();
    let mut best_idx = op_indices[0];
    let mut best_diff = springs.len() as i32;
    let mut ndq_left = 0;
    let mut ndq_right = 0;
    for idx in op_indices {
        let ndq_left_curr = springs[..idx].iter().filter(|c| **c != '.').count() as i32;
        let ndq_right_curr = springs[idx+1..].iter().filter(|c| **c != '.').count() as i32;
        let diff = (ndq_left_curr - ndq_right_curr).abs();
        if diff < best_diff {
            best_idx = idx;
            best_diff = diff;
            ndq_left = ndq_left_curr;
            ndq_right = ndq_right_curr;
        }
    }

    let springs_left = springs[..best_idx].to_vec();
    let springs_right = springs[best_idx+1..].to_vec();

    n_ways_clean_split(springs_left, springs_right, group_sizes, ndq_left, ndq_right)
}

pub fn n_ways_clean_split(springs_left: Vec<char>, springs_right: Vec<char>, group_sizes: &Vec<usize>, 
    ndq_left: i32, ndq_right: i32) -> u64 {
    let nd_left = springs_left.iter().filter(|c| **c == '#').count() as i32;
    let nd_right = springs_right.iter().filter(|c| **c == '#').count() as i32;

    // now count the ways for each way to split up group_sizes
    let mut total = 0;
    for g_split in 0..=group_sizes.len() {
        let ng_left: i32 = group_sizes[..g_split].iter().sum::<usize>() as i32;
        let ng_right: i32 = group_sizes[g_split..].iter().sum::<usize>() as i32;
        if nd_left <= ng_left && ng_left <= ndq_left
            && nd_right <= ng_right && ng_right <= ndq_right {
                total += n_ways(&(springs_left.clone(), group_sizes[..g_split].to_vec()))
                    * n_ways(&(springs_right.clone(), group_sizes[g_split..].to_vec()));
            }
    }
    total
}

pub fn n_ways_naive((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> u64 {

    if group_sizes.len() == 0 {
        if springs.contains(&'#') {
            return 0;
        } else {
            return 1;
        }
    }
    let g1 = group_sizes[0];
    if let Some(iqd1) = springs.iter().position(|c| *c != '.') {
        if iqd1 + g1 > springs.len() {
            return 0;
        }

        let mut max_ig = springs.len() - g1;
        if let Some(idamage1) = springs.iter().position(|c| *c == '#') {
            max_ig = max_ig.min(idamage1);
        }

        let mut total = 0;
        if group_sizes.len() == 1 {
            for ig1_guess in iqd1..springs.len() {
                if possible1(&springs, ig1_guess, g1) {
                    total += 1;
                }
            }
        } else {
            for ig1_guess in iqd1..springs.len() {
                if possible(&springs, ig1_guess, g1) {
                    let i_next = ig1_guess + g1;
                    if i_next < springs.len() {
                        if springs[i_next] != '#' {
                            let sub_ways = n_ways_naive(&(springs[i_next+1..].to_vec(), group_sizes[1..].to_vec()));
                            total += sub_ways;
                        }
                    }
                }
            }
        }
        total
    } else {
        0
    }
}

pub fn reduce_from_ends((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> (Vec<char>, Vec<usize>) {
    let mut changed = true;
    let mut state = (springs.clone(), group_sizes.clone());
    
    while changed {
        changed = false;
        if let Some(state_new) = reduce_from_left(&state) {
            state = state_new;
            changed = true;
            if state.0.len() == 0 || state.1.len() == 0 {
                break;
            }
        }
        if let Some(state_new) = reduce_from_right(&state) {
            state = state_new;
            changed = true;
            if state.0.len() == 0 || state.1.len() == 0 {
                break;
            }
        }
    }
    state
}

pub fn reduce_from_left((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> Option<(Vec<char>, Vec<usize>)> {
    let g1 = group_sizes[0];
    let iq1_opt = springs.iter().position(|c| *c == '?');
    let idamage1_opt = springs.iter().position(|c| *c == '#');
    if let Some(iq1) = iq1_opt {
        if let Some(idamage1) = idamage1_opt {
            let mut i_red: usize = idamage1 + g1 + 1;
            if iq1 < idamage1 {
                let mut ig1s: Vec<usize> = Vec::new();

                for ig1_guess in 0..=idamage1 {
                    if possible(&springs, ig1_guess, g1) {
                        ig1s.push(ig1_guess);
                    }
                }

                if ig1s.len() != 1 {
                    return None;
                } else {
                    i_red = ig1s[0] + g1 + 1;
                }
            }

            if i_red + 1 > springs.len() {
                return Some((vec![], group_sizes[1..].to_vec()));
            } else {
                if i_red >= 1 {
                    // assert!(springs[i_red-1] != '#');
                    return None;
                }
                return Some((springs[i_red..].to_vec(), group_sizes[1..].to_vec()));
            }
        }
    }

    None
}

pub fn reduce_from_right((springs, group_sizes): &(Vec<char>, Vec<usize>)) -> Option<(Vec<char>, Vec<usize>)> {
    let mut s_r = springs.clone();
    let mut gz_r = group_sizes.clone();
    s_r.reverse();
    gz_r.reverse();
    if let Some((mut s, mut gz)) = reduce_from_left(&(s_r, gz_r)) {
        s.reverse();
        gz.reverse();
        Some((s, gz))
    } else {
        None
    }
}

pub fn possible_mid(s: &Vec<char>, idx: usize, gmid: usize, gleft: usize, gright: usize) -> bool {
    if idx + gmid > s.len() {
        return false;
    } else if idx + gmid == s.len() {
        if gright > 0 {
            return false;
        }
    }
    if idx > 0 {
        if s[idx-1] == '#' {
            return false;
        }
    } else {
        if gleft > 0 {
            return false;
        }
    }

    for di in 0..gmid {
        if s[idx + di] == '.' {
            return false;
        }
    }

    if idx + gmid < s.len() {
        if s[idx + gmid] == '#' {
            return false;
        }
    }

    true
}

pub fn possible(s: &Vec<char>, idx: usize, group_sz: usize) -> bool {
    if idx + group_sz > s.len() {
        return false;
    }
    for c in &s[0..idx] {
        if *c == '#' {
            return false;
        }
    }

    for di in 0..group_sz {
        if s[idx + di] == '.' {
            return false;
        }
    }

    if idx + group_sz < s.len() {
        if s[idx + group_sz] == '#' {
            return false;
        }
    }

    true
}

pub fn possible1(s: &Vec<char>, idx: usize, group_sz: usize) -> bool {
    if idx + group_sz > s.len() {
        return false;
    }
    for c in &s[0..idx] {
        if *c == '#' {
            return false;
        }
    }

    for di in 0..group_sz {
        if s[idx + di] == '.' {
            return false;
        }
    }

    for c in &s[idx+group_sz..] {
        if *c == '#' {
            return false;
        }
    }

    true
}