use std::collections::HashMap;
use std::fs;
use std::error::Error;
use std::iter::zip;

fn get_primes(max: usize) -> Vec<usize> {
    let mut is_p = vec![true; max];
    is_p[0] = false;
    is_p[1] = false;
    let mut primes = vec![];
    for i in 2..max {
        if is_p[i] {
            if i * i < max {
                let mut n = 2*i;
                while n < max {
                    is_p[n] = false;
                    n += i;
                }
            }
            primes.push(i);
        }
    }

    primes
}

fn extended_gcd(a: i64, b: i64) -> ((i64, i64), i64, (i64, i64)) {
    let (mut old_r, mut r): (i64, i64) = (a, b);
    let (mut old_s, mut s): (i64, i64) = (1, 0);
    let (mut old_t, mut t): (i64, i64) = (0, 1);
    while r != 0 {
        let quot = old_r / r;
        (old_r, r) = (r, old_r - quot * r);
        (old_s, s) = (s, old_s - quot * s);
        (old_t, t) = (t, old_t - quot * t);
    }

    ((old_s, old_t), old_r, (t, s))
}

fn chinese_remainder_thm(mods: Vec<i64>, res: Vec<i64>) -> i64 {
    let mut N: i64 = 1;
    for m in &mods {
        N *= m;
    }
    let mut x: u128 = 0;
    for (ni, r) in zip(mods, res) {
        let Ni = N / ni;
        let (bezout, _, _) = extended_gcd(Ni, ni);
        let mut b = bezout.0;
        if b < 0 {
            b += N;
        }
        // println!("try multiply {} {}({}) {}", r, bezout.0, b, Ni);

        x += r as u128 * b as u128 * Ni as u128;
    }

    return (x % N as u128) as i64;
}

fn might_collide(x1: i64, y1: i64, vx1: i64, vy1: i64, 
                 x2: i64, y2: i64, vx2: i64, vy2: i64, pmin: f64, pmax: f64) -> bool {

    // t = (x - x0)/vx = (y - y0)/vy
    // vy x - vy x0 = vx y - vx y0
    // vy x - vx y = vy x0 - vx y0 = c
    // vy1 x - vx1 y = c1 => vy1 vy2 x - vx1 vy2 y = vy2 c1
    // vy2 x - vx2 y = c2 => vy1 vy2 x - vy1 vx2 y = vy1 c2
    
    // => -det y = vy2 c1 - vy1 c2 => y = (vy1 c2 - vy2 c1) / det

    let det = vx1 * vy2 - vx2 * vy1;
    if det == 0 {
        return false;
    }

    let c1 = vy1 * x1 - vx1 * y1;
    let c2 = vy2 * x2 - vx2 * y2;
    let y: f64 = (vy1 as f64 * c2 as f64 - vy2 as f64 * c1 as f64) / det as f64;
    if y < pmin || y > pmax {
        return false;
    }
    let t1 = (y - y1 as f64) / vy1 as f64;
    if t1 < 0.0 {
        return false;
    }
    let t2 = (y - y2 as f64) / vy2 as f64;
    if t2 < 0.0 {
        return false;
    }
    let x: f64 = x1 as f64 + t1 * vx1 as f64;
    if x < pmin || x > pmax {
        return false;
    }

    true
}

fn try_mod(vj: i64, dim: usize, stones: &Vec<[i64; 6]>, primes: &Vec<usize>) -> Option<i64> {

// x[n] = x0 + n * vx (2 unknowns)

// x[ni] = xi + ni * vxi = x0 + ni * vx => 0 = (x0 - xi) + ni * (vx - vxi)

// x[n1] = x1 + vx1 * n1 = x0 + n1 * vx => x1 + vx1 * n1 = x0 (mod vx)
// x[n2] = x2 + vx2 * n2 = x0 + n2 * vx => x2 + vx2 * n2 = x0 (mod vx)

// delta x
// n = 0: xi - x0
// n = 1: xi - x0 + vxi - vx
// n = 2: xi - x0 + 2*(vxi - vx) => xi - x0 = 0 (modulo vxi-vx) => x0 = xi (modulo vxi-vx)

// if vx > vxi, makes no difference:
// x0 - xi + n*(vx - vxi) => x0 - xi = 0 (modulo vx - vxi)

    // a mod b
    let mut ab: Vec<(i64, i64)> = Vec::new();
    for s in stones {
        let m = (s[dim+3] - vj).abs();
        if m != 0 {
            let r = s[dim].rem_euclid(m);
            ab.push((r, m));
        }
    }
    ab.sort_by_key(|(_, b)| *b);

    for pair in ab[..].windows(2) {
        let (a1, b1) = pair[0];
        let (a2, b2) = pair[1];
        if (b1 == b2) && (a1 != a2) {
            return None;
        }
    }

    ab.dedup();

    let mut r_by_p: HashMap<usize, (usize, i64)> = HashMap::new();
    for &(a, b) in &ab {
        for &p in primes {
            if b as usize % p == 0 {
                let mut pow: usize = 1;
                let mut ppow = p;
                while b as usize % (p*ppow) == 0 {
                    pow += 1;
                    ppow *= p;
                }

                if r_by_p.get(&p).is_some_and(|&(ppow_old, _)| ppow > ppow_old)
                    || !r_by_p.contains_key(&p) {

                    r_by_p.insert(p, (ppow, a % ppow as i64));
                }
            }
        }
    }

    let mut N: i64 = 1;
    let mut res: i64 = 0;
    
    for &(ppow, r) in r_by_p.values() {
        if N == 1 {
            N = ppow as i64;
            res = r;
        } else {
            if N > i64::MAX / ppow as i64 {
                break;
            }
            res = chinese_remainder_thm(vec![N, ppow as i64], vec![res, r]);

            N *= ppow as i64;
        }
    }

    Some(res)
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input24.txt")?;
    let pmin = 200000000000000i64 as f64;
    let pmax = 400000000000000i64 as f64;
    // let input = fs::read_to_string("test14.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();

    let stones: Vec<[i64; 6]> = lines.iter()
        .map(|s| {
            let (s1, s2) = s.split_once(" @ ").unwrap();
            let p: Vec<i64> = s1.split(", ").map(|n| n.parse().unwrap()).collect();
            let v: Vec<i64> = s2.split(", ").map(|n| n.parse().unwrap()).collect();
            [p[0], p[1], p[2], v[0], v[1], v[2]]
        }).collect();

    let mut n_might_collide = 0;
    for i in 0..stones.len()-1 {
        for j in i+1..stones.len() {
            let [x1, y1, _, vx1, vy1, _] = stones[i];
            let [x2, y2, _, vx2, vy2, _] = stones[j];
            if might_collide(x1, y1, vx1, vy1, x2, y2, vx2, vy2, pmin, pmax) {
                n_might_collide += 1;
            }
        }
    }
    dbg!(n_might_collide);

    let primes = get_primes(1000);

    let mut total: i64 = 0;
    for dim in 0..3 {
        print!("dim {dim}: ");
        for vj in -1000i64..1000i64 {
            if let Some(res) = try_mod(vj, dim, &stones, &primes) {
                total += res;
            }
        }
    }
    dbg!(total);

    Ok(())
}