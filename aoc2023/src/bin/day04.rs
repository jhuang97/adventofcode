use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input04.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let mut points_total = 0;
    let mut n_cards: Vec<i32> = vec![1; lines.len()];
    for (i, l) in lines.iter().enumerate() {
        let (_, num_str) = l.split_once(": ").unwrap();
        let (winning_str, your_str) = num_str.split_once(" | ").unwrap();
        let winning_nums: Vec<_> = winning_str.split_whitespace().map(|s| s.parse::<i32>().unwrap()).collect();
        let your_nums: Vec<_> = your_str.split_whitespace().map(|s| s.parse::<i32>().unwrap()).collect();

        let n_match = your_nums.iter().filter(|n| winning_nums.contains(n)).count() as u32;
        if n_match > 0 {
            points_total += 2_i32.pow(n_match-1);
            for di in 0..n_match as usize {
                n_cards[i + di + 1] += n_cards[i];
            }
        }
    }

    let cards_total: i32 = n_cards.iter().sum();

    dbg!(points_total, cards_total);

    Ok(())
}