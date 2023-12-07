use std::fs;
use std::error::Error;
use std::iter::zip;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input06.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let times = lines[0]
        .split_whitespace()
        .collect::<Vec<_>>()[1..].iter()
        .map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();

    let dists = lines[1]
        .split_whitespace()
        .collect::<Vec<_>>()[1..].iter()
        .map(|x| x.parse::<i32>().unwrap()).collect::<Vec<_>>();

    let mut prod: i64 = 1;
    for (t, d) in zip(times, dists) {
        let mut n_ways = 0;
        for t_wait in 0..t {
            if t_wait * (t - t_wait) > d {
                n_ways += 1;
            }
        }
        prod *= n_ways;
    }
    dbg!(prod);

    let big_time = lines[0]
        .split_whitespace()
        .collect::<Vec<_>>()[1..].join("").parse::<i64>()?;

    let big_dist = lines[1]
        .split_whitespace()
        .collect::<Vec<_>>()[1..].join("").parse::<i64>()?;

    let radius: f64 = ((big_time as f64).powi(2)/4.0 - (big_dist as f64)).sqrt();
    let tmid = big_time as f64 / 2.0;
    let t2 = (tmid + radius).floor();
    let t1 = (tmid - radius).ceil();
    let n_ways2 = (t2 - t1 + 1.0) as u64;
    dbg!(n_ways2);

    Ok(())
}