use std::fs;
use std::error::Error;
use std::collections::HashMap;
use itertools::Itertools;


pub fn parse_card(c: char) -> Option<u32> {
    if c.is_digit(10) {
        c.to_digit(10)
    } else {
        match c {
            'T' => Some(10),
            'J' => Some(11),
            'Q' => Some(12),
            'K' => Some(13),
            'A' => Some(14),
            _ => None
        }
    }
}

pub fn parse_card_with_jokers(c: char) -> Option<u32> {
    if c.is_digit(10) {
        c.to_digit(10)
    } else {
        match c {
            'T' => Some(10),
            'J' => Some(1),
            'Q' => Some(12),
            'K' => Some(13),
            'A' => Some(14),
            _ => None
        }
    }
}

pub fn get_type(hand: &Vec<u32>) -> i64 {
    let mut hist: HashMap<u32, u32> = HashMap::new();
    for c in hand {
        *(hist.entry(*c).or_insert(0)) += 1;
    }
    let mut freqs = hist.values().cloned().collect_vec();
    freqs.sort();
    freqs.reverse();
    match freqs[0] {
        5 => 5,
        4 => 4,
        3 => if freqs[1] == 2 { 3 } else { 2 }
        2 => if freqs[1] == 2 { 1 } else { 0 }
        _ => -1
    }
}

pub fn get_type_with_joker(hand: &Vec<u32>) -> i64 {
    let mut n_joker = 0;
    let mut hist: HashMap<u32, u32> = HashMap::new();
    for c in hand {
        if *c == 1 {
            n_joker += 1;
        } else {
            *(hist.entry(*c).or_insert(0)) += 1;
        }
    }
    if n_joker == 5 {
        return 5;
    }
    let mut freqs = hist.values().cloned().collect_vec();
    freqs.sort();
    freqs.reverse();
    match freqs[0] + n_joker {
        5 => 5,
        4 => 4,
        3 => if freqs[1] == 2 { 3 } else { 2 }
        2 => if freqs[1] == 2 { 1 } else { 0 }
        _ => -1
    }
}

pub fn winnings(lines: &Vec<&str>, parse_fn: fn(char) -> Option<u32>, type_fn: fn(&Vec<u32>) -> i64) {
    let mut hand_bids: Vec<(Vec<u32>, u32)> = lines.iter()
        .map(|s| {
            let (a, b) = s.split_once(" ").unwrap();
            (a.chars().map(|x| parse_fn(x).unwrap()).collect(), b.parse().unwrap())
        }).collect();

    hand_bids.sort_by_key(|k| {
        let v = &k.0;
        (type_fn(v), v[0], v[1], v[2], v[3], v[4])
    });

    let mut total: u32 = 0;
    for (i, (_, bid)) in hand_bids.iter().enumerate() {
        total += (i as u32 + 1) * bid;
    }
    dbg!(total);
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input07.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    winnings(&lines, parse_card, get_type);
    winnings(&lines, parse_card_with_jokers, get_type_with_joker);

    Ok(())
}