use std::fs;
use std::error::Error;
use std::collections::HashMap;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input02.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let color_max = HashMap::from([
        ("red", 12),
        ("green", 13),
        ("blue", 14)
    ]);

    let mut total: i32 = 0;
    let mut total2: i32 = 0;
    for l in &lines {
        let mut parts = l.split(": ");
        let p1 = parts.next().unwrap();
        let game_id: i32 = p1.split(" ").nth(1).unwrap().parse()?;
        let p2 = parts.next().unwrap();
        let mut possible = true;
        let mut max_possible: HashMap<&str, i32> = HashMap::new();

        for draw in p2.split("; ") {
            for color_term in draw.split(", ") {
                let mut c = color_term.split(" ");
                let count: i32 = c.next().unwrap().parse()?;
                let color_name = c.next().unwrap();
                if count > *color_max.get(color_name).unwrap() {
                    possible = false;
                }
                max_possible.entry(color_name)
                    .and_modify(|n| *n = count.max(*n))
                    .or_insert(count);
            }
        }
        if possible {
            total += game_id;
        }
        let mut prod = 1;
        for val in max_possible.values() {
            prod *= val;
        }
        total2 += prod;
    }
    println!("{}", total);
    println!("{}", total2);

    Ok(())
}
