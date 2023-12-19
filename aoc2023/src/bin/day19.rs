use std::collections::HashMap;
use std::fs;
use std::error::Error;
use std::ops::RangeInclusive;
use std::str::FromStr;

#[derive(Clone)]
enum Name {
    Verdict(bool),
    Workflow(String),
}

#[derive(Debug, PartialEq, Eq)]
struct ParseNameError;

impl FromStr for Name {
    type Err = ParseNameError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(match s {
            "A" => Name::Verdict(true),
            "R" => Name::Verdict(false),
            _ => Name::Workflow(s.to_owned())
        })
    }
}

struct Condition {
    category: char,
    lt: bool,
    threshold: u32,
}

impl Condition {
    fn pass(&self, p: &Part) -> bool {
        let test_val = match self.category {
            'x' => p.x,
            'm' => p.m,
            'a' => p.a,
            's' => p.s,
            _ => unreachable!(),
        };
        if self.lt {
            test_val < self.threshold
        } else {
            test_val > self.threshold
        }
    }

    fn pass_range(&self, p: &PartRange) -> Vec<(PartRange, bool)> {
        let idx = match self.category {
            'x' => 0,
            'm' => 1,
            'a' => 2,
            's' => 3,
            _ => unreachable!(),
        };
        let p_range = &p.r[idx];
        let mut pc = p.clone();
        if self.lt {
            if *p_range.start() >= self.threshold {
                vec![(pc, false)]
            } else if *p_range.end() < self.threshold {
                vec![(pc, true)]
            } else {
                pc.r[idx] = *p_range.start()..=self.threshold-1;
                let mut pc2 = p.clone();
                pc2.r[idx] = self.threshold..=*p_range.end();
                vec![(pc, true), (pc2, false)]
            }
        } else {
            if *p_range.start() > self.threshold {
                vec![(pc, true)]
            } else if *p_range.end() <= self.threshold {
                vec![(pc, false)]
            } else {
                pc.r[idx] = *p_range.start()..=self.threshold;
                let mut pc2 = p.clone();
                pc2.r[idx] = self.threshold+1..=*p_range.end();
                vec![(pc, false), (pc2, true)]
            }
        }
    }
}

#[derive(Debug, PartialEq, Eq)]
struct ParseConditionError;

impl FromStr for Condition {
    type Err = ParseConditionError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let ((s1, s2), lt) = if s.contains(">") {
            (s.split_once(">").unwrap(), false)
        } else if s.contains("<") {
            (s.split_once("<").unwrap(), true)
        } else {
            return Err(ParseConditionError);
        };

        Ok(Self {
            category: s1.chars().nth(0).ok_or(ParseConditionError)?,
            lt,
            threshold: s2.parse::<u32>().map_err(|_| ParseConditionError)?,
        })
    }
}

struct Rule {
    cond: Option<Condition>,
    dest: Name
}

#[derive(Debug, PartialEq, Eq)]
struct ParseRuleError;

impl FromStr for Rule {
    type Err = ParseRuleError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        Ok(
            if s.contains(":") {
                let (s1, s2) = s.split_once(":").unwrap();
                Self {
                    cond: Some(s1.parse::<Condition>().map_err(|_| ParseRuleError)?),
                    dest: s2.parse::<Name>().map_err(|_| ParseRuleError)?,
                }
            } else {
                Self {
                    cond: None,
                    dest: s.parse::<Name>().map_err(|_| ParseRuleError)?,
                }
            }
        )
    }
}

struct Workflow {
    rules: Vec<Rule>
}

impl Workflow {
    fn run(&self, p: &Part) -> Name {
        for r in &self.rules {
            if let Some(c) = &r.cond {
                if c.pass(p) {
                    return r.dest.clone();
                }
            } else {
                return r.dest.clone();
            }
        }
        unreachable!()
    }

    fn run_range(&self, pr0: PartRange) -> Vec<(PartRange, Name)> {
        let mut out = Vec::new();
        let mut curr: Vec<PartRange> = vec![pr0];
        for r in &self.rules {
            if curr.is_empty() {
                break;
            }
            if let Some(c) = &r.cond {
                let mut next: Vec<PartRange> = Vec::new();
                while let Some(pr) = curr.pop() {
                    for (pr2, b) in c.pass_range(&pr) {
                        if b {
                            out.push((pr2, r.dest.clone()));
                        } else {
                            next.push(pr2);
                        }
                    }
                }
                curr.append(&mut next);
            } else {
                for pr in curr.into_iter() {
                    out.push((pr, r.dest.clone()));
                }
                break;
            }
        }
        out
    }
}

#[derive(Debug, PartialEq, Eq)]
struct ParseWorkflowError;

impl FromStr for Workflow {
    type Err = ParseWorkflowError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let items: Result<Vec<_>, _> = s.split(",").map(|x| x.parse::<Rule>()).collect();
        Ok(
            Self {
                rules: items.map_err(|_| ParseWorkflowError)?,
            }
        )
    }
}

struct Part {
    x: u32,
    m: u32,
    a: u32,
    s: u32,
}

#[derive(Debug, PartialEq, Eq)]
struct ParsePartError;

impl FromStr for Part {
    type Err = ParsePartError;

    fn from_str(s: &str) -> Result<Self, Self::Err> {
        let s2 = s
            .strip_prefix("{")
            .and_then(|x| x.strip_suffix("}"))
            .ok_or(ParsePartError)?;
        let terms: Vec<_> = s2.split(",").collect();

        Ok(Self {
            x: terms[0].strip_prefix("x=").ok_or(ParsePartError)?.parse::<u32>().map_err(|_| ParsePartError)?,
            m: terms[1].strip_prefix("m=").ok_or(ParsePartError)?.parse::<u32>().map_err(|_| ParsePartError)?,
            a: terms[2].strip_prefix("a=").ok_or(ParsePartError)?.parse::<u32>().map_err(|_| ParsePartError)?,
            s: terms[3].strip_prefix("s=").ok_or(ParsePartError)?.parse::<u32>().map_err(|_| ParsePartError)?,
        })
    }
}

#[derive(Debug, Clone)]
struct PartRange {
    r: [RangeInclusive<u32>; 4],
}

impl PartRange {
    fn size(&self) -> u64 {
        let mut prod = 1;
        for r in &self.r {
            prod *= (r.end() - r.start() + 1) as u64;
        }
        prod
    }
}

fn main() -> Result<(), Box<dyn Error>> {
    let input = fs::read_to_string("input19.txt")?;
    // let input = fs::read_to_string("test19.txt")?;

    let (w_s, p_s) = input.trim().split_once("\n\n").unwrap();

    let mut workflows: HashMap<String, Workflow> = HashMap::new();
    for line in w_s.lines() {
        let (name_s, workflow_s) = line.split_once("{").unwrap();
        workflows.insert(name_s.to_owned(), workflow_s.strip_suffix('}').expect("oh no").parse::<Workflow>().unwrap());
    }

    let parts: Vec<Part> = p_s.lines().map(|s| s.parse::<Part>().unwrap()).collect();

    let mut total: u32 = 0;
    for p in &parts {
        let mut res = Name::Workflow("in".to_owned());
        loop {
            match res {
                Name::Verdict(b) => {
                    if b {
                        total += p.x + p.m + p.a + p.s;
                    }
                    break;
                }
                Name::Workflow(s) => {
                    res = workflows.get(&s).unwrap().run(p)
                }
            }
        }
    }
    dbg!(total);

    let mut ranges = vec![(PartRange {r: [1..=4000, 1..=4000, 1..=4000, 1..=4000]}, Name::Workflow("in".to_owned()))];
    let mut total2: u64 = 0;
    while let Some((pr, res)) = ranges.pop() {
        match res {
            Name::Verdict(b) => {
                if b {
                    total2 += pr.size();
                }
            }
            Name::Workflow(s) => {
                ranges.append(&mut workflows.get(&s).unwrap().run_range(pr));
            }
        }
    }
    dbg!(total2);

    Ok(())
}