use std::collections::{HashMap, VecDeque};
use std::fs;
use std::error::Error;

#[derive(Debug, Clone, Copy, Eq, PartialEq)]
pub enum Pulse {
    High,
    Low
}

#[derive(Debug)]
pub enum Type {
    Broadcaster,
    Untype,
    FlipFlop(bool),
    Conjunction(HashMap<String, Pulse>),
}

#[derive(Debug)]
pub struct Module {
    outputs: Vec<String>,
    t: Type,
}

impl Module {
    fn process_pulse(&mut self, sender: String, p: &Pulse) -> Vec<(Pulse, String)> {
        let maybe_pulse: Option<Pulse> = 
        match self.t {
            Type::Broadcaster => Some(p.clone()),
            Type::Untype => None,
            Type::FlipFlop(ref mut is_on) => {
                match p {
                    Pulse::High => None,
                    Pulse::Low => {
                        *is_on = !*is_on;
                        Some(if *is_on { Pulse::High } else { Pulse::Low })
                    },
                }
            },
            Type::Conjunction(ref mut recent) => {
                recent.insert(sender, p.clone());
                let mut to_send = Pulse::Low;
                for val in recent.values() {
                    if *val == Pulse::Low {
                        to_send = Pulse::High;
                        break;
                    }
                }
                Some(to_send)
            }
        };
        if let Some(out_p) = maybe_pulse {
            (&self.outputs).iter().cloned().map(|s| (out_p, s)).collect()
        } else {
            vec![]
        }
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input20.txt")?;
    // let input = fs::read_to_string("test20.txt")?;
    // let input = fs::read_to_string("test20_2.txt")?;

    let lines: Vec<&str> = input.trim().split("\n").collect();
    let mut modules: HashMap<String, Module> = HashMap::new();
    let mut modules_from: HashMap<String, Vec<String>> = HashMap::new();

    for l in &lines {
        let (from_s, to_s) = l.split_once(" -> ").unwrap();
        let name = if &from_s[..1] == "%" || &from_s[..1] == "&" {
            &from_s[1..]
        } else { from_s };
        let to_names: Vec<String> = to_s.split(", ").map(String::from).collect();
        let t: Type = if from_s == "broadcaster" { Type::Broadcaster }
            else if &from_s[..1] == "%" { Type::FlipFlop(false) }
            else if &from_s[..1] == "&" { Type::Conjunction(HashMap::new()) }
            else { unreachable!() };
        for to_name in &to_names {
            (*modules_from.entry(to_name.clone()).or_insert(Vec::new())).push(name.to_owned());
        }
        modules.insert(name.to_owned(), Module { outputs: to_names, t });
    }

    for (module, m_from) in &modules_from {
        if !modules.contains_key(module) {
            modules.insert(module.clone(), Module { outputs: vec![], t: Type::Untype });
        }
        if let Type::Conjunction(ref mut in_map) = modules.get_mut(module).unwrap().t {
            for m_from_name in m_from {
                in_map.insert(m_from_name.clone(), Pulse::Low);
            }
        }
    }

    let mut n_low = 0;
    let mut n_high = 0;
    let mut n_button_rx: Option<usize> = None;
    let mut n_btn_high: HashMap<String, Vec<usize>> = HashMap::new();

    for k in 1..=10000 {
        let mut pulse_q: VecDeque<(String, Pulse, String)> = VecDeque::from([("button".to_owned(), Pulse::Low, "broadcaster".to_owned())]);
        while let Some((m_from, p, m_to)) = pulse_q.pop_front() {
            *(match p { Pulse::Low => &mut n_low, Pulse::High => &mut n_high }) += 1;

            if m_to == "rx" && p == Pulse::Low && n_button_rx == None {
                n_button_rx = Some(k);
            }

            if m_to == modules_from.get("rx").unwrap()[0] && p == Pulse::High {
                // println!("press #{k}, high from {m_from}");
                (*n_btn_high.entry(m_from.clone()).or_insert(Vec::new())).push(k);
            }

            // println!("{} {:?} {}", &m_from, &p, &m_to);
            let new_pulses: Vec<(String, Pulse, String)> = modules.get_mut(&m_to).unwrap().process_pulse(m_from, &p)
                .iter()
                .map(|(p, s)| (m_to.clone(), *p, s.clone()))
                .collect();
            pulse_q.append(&mut VecDeque::from(new_pulses));
        }

        if k == 1000 {
            // dbg!(n_low, n_high);
            let prod = n_low as u64 * n_high as u64;
            dbg!(prod);
        }
    }

    // dbg!(n_btn_high);
    let mut prod2: u64 = 1;
    for v in n_btn_high.values() {
        assert!(v[0] * 2 == v[1]);
        prod2 *= v[0] as u64;
    }
    dbg!(prod2);

    // dbg!(&modules_from.get("rx").unwrap()[0]);
    // dbg!(modules.get("zh").unwrap());
    // dbg!(modules_from.get("zh").unwrap());

    // dbg!(n_button_rx);

    Ok(())
}