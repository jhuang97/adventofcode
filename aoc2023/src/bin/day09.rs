use std::fs;
use std::error::Error;

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input09.txt")?;
    let lines: Vec<&str> = input.trim().split("\n").collect();

    let histories: Vec<Vec<i64>> = lines.iter()
        .map(|l| l.split_whitespace().map(|x| x.parse().unwrap()).collect())
        .collect();

    let total: i64 = histories.iter().map(|h| extrapolate(&h, true)).sum();
    dbg!(total);
    let total: i64 = histories.iter().map(|h| extrapolate(&h, false)).sum();
    dbg!(total);

    Ok(())
}

fn extrapolate(v: &Vec<i64>, forward: bool) -> i64 {
    let mut vs: Vec<Vec<i64>> = Vec::new();
    vs.push(v.clone());
    loop {
        let diffs: Vec<i64> = vs[vs.len()-1].windows(2).map(|sl| sl[1]-sl[0]).collect();
        vs.push(diffs.clone());
        if diffs.iter().all(|&x| x == 0) {
            break;
        }
    }
    vs.reverse();

    let mut n: i64 = 0;
    for i in 1..vs.len() {
        if forward {
            n += vs[i][vs[i].len()-1];
        } else {
            n = vs[i][0] - n;
        }
    }
    n
}