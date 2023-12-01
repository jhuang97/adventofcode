use std::fs;
use std::error::Error;

const WORDS: [&str; 9] = ["one", "two", "three", "four", "five", "six", "seven", "eight", "nine"];

pub fn digit_first(s: &str) -> u32 {
    for (i, c) in s.chars().enumerate() {
        if c.is_numeric() {
            return c.to_digit(10).unwrap();
        } else {
            for (iw, w) in WORDS.into_iter().enumerate() {
                if s.len() - i >= w.len() {
                    if &s[i..(i+w.len())] == w {
                        return (iw+1).try_into().unwrap();
                    }
                }
            }
        }
    }
    0
}

pub fn digit_last(s: &str) -> u32 {
    for (i, c) in s.chars().rev().enumerate() {
        if c.is_numeric() {
            return c.to_digit(10).unwrap();
        } else {
            for (iw, w) in WORDS.into_iter().enumerate() {
                if s.len() - i >= w.len() {
                    if &s[(s.len()-i-w.len())..(s.len()-i)] == w {
                        return (iw+1).try_into().unwrap();
                    }
                }
            }
        }
    }
    0
}

pub fn char_first(s: &str) -> u32 {
    for c in s.chars() {
        if c.is_numeric() {
            return c.to_digit(10).unwrap();
        }
    }
    0
}

pub fn char_last(s: &str) -> u32 {
    for c in s.chars().rev() {
        if c.is_numeric() {
            return c.to_digit(10).unwrap();
        }
    }
    0
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input01.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let mut total: u32 = 0;
    for l in &lines {
        total += char_first(l)*10 + char_last(l);
    }
    println!("{}", total);

    let mut total2: u32 = 0;
    for l in lines {
        total2 += digit_first(l)*10 + digit_last(l);
    }
    println!("{}", total2);

    Ok(())
}
