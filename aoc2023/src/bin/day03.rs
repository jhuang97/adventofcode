use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input03.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let nr = lines.len();
    let nc = lines[0].len();

    let mut symbols: HashMap<(usize, usize), char> = HashMap::new();
    let mut nums: HashMap<(usize, usize), i32> = HashMap::new();
    for (r, l) in lines.iter().enumerate() {
        let mut col_start: usize = 0;
        let mut cur_num = 0;
        let mut is_num = false;
        for (col, ch) in l.chars().enumerate() {
            if ch.is_digit(10) {
                let this_d: usize = ch.to_digit(10).unwrap() as usize;
                if is_num {
                    cur_num = cur_num * 10 + this_d;
                } else {
                    col_start = col;
                    cur_num = this_d;
                    is_num = true;
                }
            }
            if is_num && (!ch.is_digit(10) || col == l.len()-1) {
                is_num = false;
                nums.insert((r, col_start), cur_num as i32);
            }
            if !ch.is_digit(10) && ch != '.' {
                symbols.insert((r, col), ch);
            }
        }
    }

    let mut total = 0;
    for (pos, num) in &nums {
        if is_part_number(pos, num, &symbols) {
            total += num;
        }
    }

    let mut gear_neighbors: HashMap<(usize, usize), Vec<i32>> = HashMap::new();
    for (pos, num) in &nums {
        for pos_n in num_neighbors_pos(pos, num) {
            if let Some(symbol) = symbols.get(&pos_n) {
                if *symbol == '*' {
                    (*gear_neighbors.entry(pos_n).or_insert(Vec::new())).push(*num);
                }
            }
        }
    }

    let mut total2 = 0;
    for (_, neighbor_nums) in gear_neighbors {
        if neighbor_nums.len() == 2 {
            total2 += neighbor_nums[0] * neighbor_nums[1];
        }
    }

    dbg!(total, total2);

    Ok(())
}

pub fn num_neighbors_pos(pos: &(usize, usize), num: &i32) -> Vec<(usize, usize)> {
    let mut neighbors = Vec::new();
    let num_chars = num.to_string().len();
    let c1 = if pos.1 == 0 { 0 } else { pos.1 - 1 };
    let c2 = pos.1 + num_chars;
    if pos.0 >= 1 {
        for c in c1..=c2 {
            neighbors.push((pos.0-1, c));
        }
    }
    for c in c1..=c2 {
        neighbors.push((pos.0+1, c));
    }
    if pos.1 >= 1 {
        neighbors.push((pos.0, pos.1-1));
    }
    neighbors.push((pos.0, c2));

    neighbors
}


pub fn is_part_number(pos: &(usize, usize), num: &i32, symbols: &HashMap<(usize, usize), char>) -> bool {
    for pos_n in num_neighbors_pos(pos, num) {
        if symbols.contains_key(&pos_n) {
            return true;
        }
    }
    false
}
