package adventOfCode;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Map.Entry;
import java.util.PriorityQueue;

public class Day6_UniversalOrbitMap {

	public static class OrbitTree {
		public OrbitTree(HashMap<String, ArrayList<String>> children,
				HashMap<String, String> parent) {
			this.weights = new HashMap<>();
			this.children = children;
			this.parent = parent;
		}

		HashMap<String, Integer> weights;
		HashMap<String, ArrayList<String>> children;
		HashMap<String, String> parent;
		
		public int get_weight(String body) {
			if (weights.containsKey(body)) return weights.get(body);
			if (!parent.containsKey(body)) {
				weights.put(body, 0);
				return 0;
			} else {
				int wt = get_weight(parent.get(body)) + 1;
				weights.put(body, wt);
				return wt;
			}
		}
		
		public int total_weight(HashSet<String> bodies) {
			this.get_weight("COM");
			for (String s : bodies) {
				get_weight(s);
			}
			int sum = 0;
			for (Entry<String, Integer> e : weights.entrySet()) {
				sum += e.getValue();
			}
			return sum;
		}
		
		public ArrayList<String> neighbors(String a) {
			if (children.containsKey(a)) {
				ArrayList<String> out = new ArrayList<String>(children.get(a));
				if (parent.containsKey(a)) out.add(parent.get(a));
				return out;
			} else {
				ArrayList<String> out = new ArrayList<String>();
				if (parent.containsKey(a)) out.add(parent.get(a));
				return out;
			}
		}
		
		public int dist(String a, String b) {
			// search from a to b
			HashMap<String, Integer> dists = new HashMap<>();
			HashMap<String, String> prevs = new HashMap<>();
			PriorityQueue<String> unexplored = new PriorityQueue<>();
			
			dists.put(a, 0);
			unexplored.add(a);
			String next;
			String prev = null;
			while((next = unexplored.poll()) != null) {
				if (next != a) {
					prev = prevs.get(next);
					dists.put(next, dists.get(prev)+1);
					if (next == b) {
						return dists.get(prev)+1;
					}
				}
				ArrayList<String> toExplore = neighbors(next);
				for (String s : toExplore) {
					if (!dists.containsKey(s) && !unexplored.contains(s)) {
						unexplored.add(s);
						prevs.put(s, next);
					}
				}
			}
			return -1;
		}
	}
	
	public static void main(String[] args) {
		String[] centers = new String[]{"LH2","SSV","G9G","XN6","D8D","7ZK","6VH","N1T","2TN","VQ9","JXH","FPY","VFX","182","PN1","K3N","VBB","PMC","P8H","ZCY","8HH","3VL","C39","79Z","Z1V","PFW","RG5","99C","RNK","L1L","KS5","PY4","H9Z","8FX","HYD","XB3","PFF","LRM","SH2","GH8","D86","5RC","WNM","7K2","3P1","KV5","N4J","JRS","5BL","FDJ","JB5","SZ8","3D1","TYZ","NJT","YVK","TYG","PLM","NS5","NW3","NY5","2RR","RDY","Q4S","TS5","S6M","2X8","2D3","1YX","P6B","PNW","T3B","HR8","R76","C1G","CZJ","663","WSX","NRR","CK1","DN1","XLQ","6ZC","FRD","R9J","NSP","7KD","FMJ","JNZ","D7J","MBF","PJG","M5Q","KYL","DKT","XVN","13W","MLH","977","Z7Y","XRS","8ZH","L4D","PDM","N4N","45K","6NS","QK9","2TC","1S1","YFJ","694","KCY","H43","WZK","8H3","3TK","77C","86V","X3T","L7Y","PLG","NRR","WW4","FVJ","3K9","DPN","W6P","VQ7","ZKQ","TJN","LQL","GG1","R88","DRF","133","GMG","SXW","SHM","VJV","2DZ","MRL","N7H","VK6","XTW","SC7","3FK","4DY","8NB","2X9","X8L","TJT","RHX","HGH","FDZ","5BM","COM","YS2","M9H","Z9M","H84","BHW","32Y","1QL","ZWT","W3B","F4L","LVR","984","S3X","PJK","TYH","8CS","VPL","TD2","2L5","K2B","KNS","KCF","C2D","Z7C","DGR","LHC","WKQ","938","QZF","DBK","B6P","TPC","39W","HRD","XM9","HMD","FBR","1XM","C6D","YJ1","5YT","6MW","WHM","MHB","G47","RG7","WPM","P5H","Z7T","RGM","KKV","F88","93B","YXH","CST","QLQ","4M8","KN8","KFG","F8J","538","6X9","8G8","LYW","XCG","SK3","H1W","SH5","15T","7FF","Q4F","CSN","Z9Z","98R","G23","Z9M","NKD","DYW","PH9","JNZ","ZNS","6JQ","ZX6","DJ8","2Y8","1PY","5BB","F6Z","CPH","Z1W","H2Q","HD7","QYB","V91","DTF","W1W","8CH","WN5","1K8","FD7","PR1","JJ8","42Y","69Q","WKP","P65","2HQ","KPK","N2T","1MX","6DN","7QG","38R","3SN","3ZF","HS9","2YJ","NNH","Z23","B52","3PY","31M","RNQ","S6S","4H4","4DG","2TR","Q21","5RC","6D7","54J","RJ7","D64","FFF","11T","D9H","2M8","PQ7","NTH","X5R","M86","9FD","FDJ","QFR","NQT","KZY","Y5L","K2Z","9F2","WNT","4QV","B4G","W97","7R1","VXX","1ST","M6H","2X8","3P3","NJH","52F","NWC","HYP","4XT","52B","JXQ","MVT","GWY","P1D","ZXY","D74","9CK","K25","718","QS1","PJT","Y1C","NBW","9TT","VDS","K4S","RXC","9RT","WFT","2XH","QFC","342","3H3","5FD","XDC","X86","6YT","R8M","G7X","MGB","2NZ","W4M","D9K","VD2","LMC","Z5Q","PGP","454","HXP","FHG","SSL","FXB","M9V","XLK","24H","ZXS","F2D","MJR","38H","D6F","TQB","L35","MG6","8M5","CNN","KZJ","TCC","M3Q","RLX","2BW","WYW","WYF","2V5","GVF","4TC","CK1","QWQ","FLQ","B8T","6RP","N4P","3P3","692","PT7","HLB","JX7","WCM","XFX","JDC","W93","T44","ZRG","YVN","YFJ","L79","YQJ","412","JZW","RR6","S13","MLH","DZ1","49J","Z11","C8V","YC2","L6R","47W","Q9B","F2X","ZW5","W1X","96M","N59","6Z8","ZKB","LSH","294","BML","QK9","17Q","WJT","SY4","Z7M","C8H","X5H","SC7","Z47","SKJ","CSX","QCD","11V","KTY","TB8","Y9G","XG3","KND","JYH","59K","4R2","HV5","RHL","DZ1","3GS","GLB","V2M","SP6","BXW","L6P","H11","73C","BSN","1XT","1J9","331","CVT","F47","G8V","3GB","L74","73M","N28","XYF","7K7","6DB","8PC","9TJ","44H","NHN","QYW","RSP","M7S","6N1","P1L","VWY","NNH","894","S3X","6SS","9P7","ZZK","XXP","1K8","9FS","7HQ","J7V","43C","HM7","F7J","K35","84W","4JW","G4N","Q39","C8J","B7L","DK3","3S4","TN4","RYX","TDL","8VR","11X","THB","RP3","RHY","NSH","CP6","7KF","5BG","NPD","JL1","1CM","KXH","T87","R7B","B7P","6PR","2VD","BZ5","HYM","MBY","BZ1","J6F","T32","D4X","D7P","8GG","GPH","V6J","77D","5JD","JDC","64J","XJ4","T22","1DV","PSB","77Y","NXD","NZD","QTR","3K9","56N","3PN","47W","745","THB","742","6FM","ZFK","FCB","1PH","SL4","72S","LHK","7ZC","6K4","741","CGX","PNQ","1XR","V8F","DLB","PJN","HCZ","Z43","F44","81D","51V","QZS","NTG","Y99","GPK","1DV","C81","6S4","6YY","73C","JYH","QZ6","61S","4BC","453","5XX","M4T","JZW","3TY","JMF","YN4","PWY","PJN","BGX","Y8W","X72","82J","5TR","2G9","4XX","MB8","W1H","6Q7","RNN","97G","5MZ","12N","5X8","4K6","MTD","VJJ","QXR","4R1","T8Z","ZVS","K1R","Q5V","VY4","W6L","5YQ","HWR","LJK","Y4V","5SD","95M","BSQ","M2R","TVD","BQ6","7D3","ZX6","ZF3","VP9","PFF","PD4","292","QL6","SCV","TKD","2TK","8HM","7YN","Z2K","M9H","ZMT","KRW","1CK","KC6","785","XL4","R8F","8GK","N2W","2DZ","FPQ","PJC","CJF","8NT","RGS","8NY","W2K","WNB","X86","R3Z","8JP","J28","DWH","791","GLN","CTW","KR7","V5V","Q6T","P9N","MGX","7JQ","TZH","K32","JNG","39G","4LY","P56","N3W","YPJ","L17","DFK","44Q","QNC","KKY","78W","C14","DBC","9JN","ZSY","3H9","XVH","C95","7PH","1XC","7JT","1CD","G1T","SDG","XLB","9BJ","F88","6S2","B4R","CWF","JXK","HQY","8TP","BFY","XTK","CLN","WBZ","JP5","3PJ","F7T","KY8","18J","SNS","V55","VW7","T23","RVW","7PX","5TY","DXF","9SD","CWN","GDH","NRC","HWL","HM7","VXQ","N47","THY","9V7","331","GWL","V8K","23R","897","QSV","SSV","PJK","Z6S","RQX","J43","9Y8","1LK","SST","94K","47Q","PJC","X7N","3HR","FGV","YTR","4LZ","JSK","1FM","TQL","BJP","KS5","VJX","QTW","M6P","YXK","GR9","Z7R","2V5","5V5","TB9","65V","QGQ","31D","RZX","BPG","8X6","HYR","9GG","H7M","Q6T","V8F","P96","DN8","SPV","LTD","FYT","MRL","JNM","H1S","F8N","8TG","3G5","5MB","C8H","YJR","7PD","GK3","7R1","5PW","7CT","MPS","6D8","YN4","PT7","72B","7S6","6P5","6TP","BTL","Y31","N87","PFG","Y2D","B5Z","38J","4XT","J25","4BC","8X6","GTK","2DC","WV8","YRM","XXF","921","YWG","2KN","389","6YQ","R7S","TTR","ZRQ","3LJ","273","6YK","YZB","X7S","PWR","VLF","T22","Q9B","RH4","JP8","ZNR","N8M","KR4","G9K","X4P","XLY","DS6","CRT","F6P","24N","DQ5","SQG","YMF","BLC","B3S","YW1","YWQ","6XR","R3Z","3H8","KDR","CZ3","B6G","D9B","4Q5","MZD","QVM","HD7","TDG","LD6","ZF4","Y6X","9F2","79T","BJ8","VLF","6QY","LYW","D6J","3CJ","LNJ","2C7","TJ7","V74","VHD","8P7","PCG","D1X","745","1GC","TXB","Y3X","DQR","JNG","Z54","NWZ","9N1","MWB","BN3","K94","K4Y","9HP","1XY","YZ3","QN1","Z18","D94","VVH","84Z","S1C","BJ4","MTT","D7T","9VN","MQV","3RW","WYC","HSM","5GT","PTG","TTD","1G2","FPQ","BPG","RN6","F2X","2TR","BB6","52Y","4NH","M4L","Z7L","P1W","9HX","PQB","9YR","H7T","WDP","3PN","5XX","X5H","VK6","8XM","CNV","3XQ","T9F","R5B","1Z7","YZB","LRN","HWL","N8K","99W","1LK","HSQ","V7P","QZ8","FQ5","2N6","RS6","34G","LD9","496","BN6","BM7","4H4","86W","T4H","Z3W","CK7","6H9","X4W","D5V","KPM","GBY","8X3","11T","GBZ","M3V","C5B","7HQ","PN6","JC4","95D","WJM","92S","GBZ","R74","2ZJ","L49","RCZ","KCZ","QYW","4NL","ZKD","XQ3","K4S","8XM","785","JFL","4XK","ZSN","F15","9S1","6RP","NJK","DQ5","99Y","45D","65K","DXW","MTT","J55","R88","3X6","XDH"};
		String[] orbiters = new String[]{"LD6","S13","LNJ","BNR","K4S","C14","FRD","DPN","43C","YJR","5BL","WCM","PJC","1GK","2KN","3HR","4XX","NW3","6DB","2XH","WPM","NTH","NNH","JZW","9RT","KV5","9F2","PTG","GBZ","TZH","FFF","NHN","K35","4NL","27S","8TG","JNG","7ZK","MTD","H7M","Q5V","RXC","D6F","8HM","9JN","LVR","F4L","ZNS","MWB","BFY","XQ3","J6F","WW4","54J","NRC","SCV","SK3","P6B","Z2K","3P3","L74","RG5","3X6","977","XL4","1CD","VDS","R4G","PWR","4DY","KR4","XCG","B4R","JH1","Z47","4H4","538","KCF","CNN","BHW","72S","H1S","KKY","NRR","24N","8GG","CSN","21F","X4P","MGX","VQ9","34G","WNM","RDY","9CK","WJM","MHB","1F7","4JW","5CN","3SN","CTW","RNQ","NZD","938","RGS","8X6","HMD","CLN","W6L","KY8","W93","F35","2Y8","9PD","31M","ZWT","PCG","741","3XQ","QFR","HWR","XJ4","ZF3","R8F","F6Z","Y4V","KCY","4XK","N87","JSK","RCB","D1X","HYP","LSH","G9K","RGM","32Y","JXK","S3X","DZ1","B52","B3S","73M","6RP","ZF4","VFX","454","H11","8FX","6SS","ZKD","M3V","Z7R","PJK","45K","BM7","D74","RHX","QK9","F7J","N7H","M9H","XVN","7ZC","Z3W","6JQ","N4J","LHK","YWQ","PT7","PN1","694","FPY","BJ8","897","6FM","K4Y","N2T","9HP","HS9","99W","5MZ","77Y","9BX","DBK","VXQ","WKP","6VH","5WM","KDR","82J","1XM","R88","L17","CST","YRM","1K8","9C4","W1X","17Q","FYT","BB6","V8B","PQ7","7JQ","1GC","TB9","8JP","TVD","BF2","4NH","TS5","P96","KS5","42Y","PFG","MTT","81D","V8F","B6G","Q21","2D3","VJV","ZSY","Y5L","2YJ","YXH","PQS","PLG","65K","Q9B","M4T","Y99","F2X","J7V","Z5Q","YVN","GR9","FQ5","692","99C","QZ8","2NZ","X4W","VD2","4TC","1Z7","5FD","FVJ","R76","LH2","7R1","9GG","6P5","496","P56","5V5","M5Q","QGQ","HV5","D86","RCZ","GWL","X8L","L6R","NJT","PNW","GLN","M4L","XXP","RHY","QXR","V91","HSM","77C","RNK","PWY","N4P","P8H","PFF","NY5","6YY","ZKQ","XLQ","WYW","WYC","KFG","Z1V","9V7","V6J","TYG","8HK","XYF","4DG","12N","49J","YVK","SAN","CWN","PJG","WSX","6MQ","TTR","V55","LYW","D94","TDL","ZBY","4QV","1XY","TN4","PLM","QL6","YC2","C39","ZRQ","K2Z","DGR","VVH","2TC","2TR","YZ3","RJ7","SQG","8Z8","8M5","RPC","9BJ","NWZ","6J5","YMF","N1T","HXP","WDP","K32","XB3","Z43","RR6","N4N","RP3","JNZ","FBR","B4G","QZS","3VL","DXW","T32","8TP","ZNR","W62","PH9","GG1","NSP","1G2","QC3","N8Q","YJ1","FPQ","6JD","69Q","331","Y1C","7HQ","JDB","5JD","T1L","SL4","LD9","R8M","W6P","39G","V7P","292","G7X","HD7","T3B","W97","6S4","TJN","QZ6","SST","HCZ","5MB","6X9","ZJ2","L6P","MG6","DBC","56N","FNW","5YQ","NWC","4R1","K3N","2VD","G6M","HRD","D7J","9FD","DKT","VHD","TDG","M6H","SKJ","44H","VW7","38H","5TR","11T","3LM","3H8","FGV","2BW","6Z8","4R2","KXH","3PJ","BN6","2N6","T44","Y2D","SP6","921","2TN","H2Q","3TK","GH8","C81","PY4","X5R","1PY","V5V","PDM","2PG","XVH","NBW","RQX","389","KZY","51V","MVT","3G5","6YK","P1D","8HH","DN8","MBF","WJT","V34","YWG","XN6","X5H","VP9","785","SNS","1XC","8XM","6TP","TQL","N47","HYR","H1W","663","KYL","RN6","V2M","YQJ","L7Y","TYZ","3H9","3LJ","5PW","XM9","JX7","7D3","GTK","2X9","BJ4","8G8","9YR","93B","QS1","15T","VQ7","D8D","K25","6H9","TYH","D7T","G1T","R7B","23R","ZRG","9TJ","5VF","8P7","3FK","M9V","BGX","MLH","D7X","GBY","894","DXF","45D","JMF","7YN","L1L","T4H","QYB","R74","Y31","MB8","SXW","SPV","Z7Y","KC6","453","7CT","7KD","QTW","SJS","84Z","WN5","G9G","YXK","3GD","SH5","5BM","T24","342","7PH","2L5","KPM","B7L","NTG","1CM","1YX","W2K","B5Z","DN1","YZB","84W","W1H","LTD","QN1","6N1","KZ4","F9J","TXB","M6P","J28","52B","VY4","D9K","XTK","4Q5","11V","B8T","6MW","47Q","ZSN","JJ8","3RW","BZ5","9FS","DYW","3PY","1DV","FHG","9HX","RYX","T8Z","7JT","C8H","L49","YN4","MBY","JP8","L4D","6NS","LQL","RZX","Y8W","BQ6","Z1W","S6S","133","CNV","FXB","BSN","52Y","38J","5YT","BZ1","NPD","18J","T22","H6K","4BC","BLC","HGH","GWY","DQ5","X3T","MGB","C5B","791","CRT","Z7M","13W","7FF","JFL","8GK","3CJ","HM7","XFX","2RR","31D","Z9Z","8VR","XXF","QLQ","73C","W3B","FLQ","FDJ","Q4S","8NT","CK7","F2D","2M8","4ZC","Q4F","CJF","CWF","97G","XLY","M3Q","79T","GPH","G47","VJX","B5R","RLX","D5V","9Y8","TTD","TJT","1MX","JC4","6K4","2TK","XTW","HYD","9SD","8PC","1QL","8NY","N8K","JDC","6XR","VK6","KPK","6DN","FD7","JNM","RRT","RNN","CP6","KND","MZD","JP5","7TL","DQR","QFC","KRW","P9N","Y3S","8RW","D7P","GDH","P1W","X72","RVW","Y3X","BSQ","BTL","Y6X","TCC","DFK","QWQ","F7T","PRQ","X86","412","2G9","2HQ","M7S","8CS","M2L","KR7","CGX","2WD","7S6","3PN","DTF","D6J","6YQ","JXH","Z9M","F88","SSL","ZCY","WBZ","Z7T","F47","5X8","98R","PJN","H84","742","JXQ","ZZK","V74","V8K","H7T","QYW","RS6","86W","984","2DZ","72B","GVF","4K6","FMJ","39W","BN3","VPL","ZVS","8X3","MXQ","J43","96M","YPJ","6Q7","JCY","PNQ","3B6","PTH","N28","N59","NKD","R9J","7PD","SZ8","38R","ZX6","N3W","BPG","QNC","F15","8ZH","Z7L","NSH","CZ3","THY","ZMT","Z23","DWH","KTY","99Y","6YT","T23","1FM","44Q","K37","C6D","65V","8NB","6QY","6PR","D4X","BXW","B7P","K94","VXX","4XT","QVM","WZK","95D","DK3","HWF","9N1","DJ8","92S","LRN","C8V","Z18","DLB","11X","NXD","X7S","2LH","N8M","745","XDH","4CG","PFW","CSX","ZFK","TDF","1PH","R7S","Y9G","XLK","CVT","DRF","2X8","NHC","Q6T","P5H","L79","3TY","XRS","NS5","YOU","273","PN6","QCD","KN8","TQB","X7N","VLF","3GS","WHM","3S4","1ST","G73","7PX","HWL","1MZ","QSV","LRM","WNT","SSV","T87","YW1","C8J","24H","JB5","N2W","1XT","294","7K7","K2B","B6P","6D8","8H3","5SD","94K","95M","S1C","F8N","YFJ","KKV","M2R","NJH","GLB","MPS","JM8","R5B","9P7","5PD","RSP","SC7","VJJ","NQT","6D7","M86","GPK","HYM","PJT","5XX","B6F","59K","4LZ","ZKB","2DC","K1R","3GB","6S2","47W","NJK","Z54","HWW","G4N","JYH","XLB","LJK","SDG","4LY","3K9","PSB","SY4","3ZF","MQV","C1G","PMC","GK3","K8J","CK1","P65","HR8","SHM","KCZ","6RC","YS2","5TY","C95","C2D","1S1","HY1","XG3","1LK","HSQ","PR1","W1W","86V","MRL","FV2","7QG","5GT","TB8","XDC","TD2","VWY","L35","WFT","Q39","FDZ","5BG","9VN","ZW5","KNS","9S1","7KF","WYF","HQY","D9H","RHL","9TT","CZJ","F8J","H9Z","3H3","SH2","Z7C","7K2","S6M","QTR","TKD","J55","MJR","TPC","ZXY","ZXS","J25","T9F","1CK","8CH","LMC","D9B","FCB","718","77D","THB","5RC","4VQ","HLB","D64","G8V","5BB","CPH","VBB","X2L","2V5","YTR","RG7","4M8","7NZ","WKQ","6ZC","PQB","PD4","F44","BJP","TJ7","3P1","LHC","Z6S","RH4","KZJ","WV8","H43","2C7","Z11","1XR","P1L","DNX","182","78W","61S","3D1","GMG","2ZJ","PGP","R3Z","1J9","JL1","QZF","S1J","52F","WNB","F6P","79Z","SDY","JRS","BML","FQH","G23","DS6","64J","W4M"};
		HashMap<String, ArrayList<String>> children = new HashMap<>();
		HashMap<String, String> parent = new HashMap<>();
		HashSet<String> bodies = new HashSet<>();
		for (int i = 0; i < centers.length; i++) {
			bodies.add(orbiters[i]);
			bodies.add(centers[i]);
			parent.put(orbiters[i], centers[i]);
			if (children.containsKey(centers[i])) {
				children.get(centers[i]).add(orbiters[i]);
			} else {
				ArrayList<String> al = new ArrayList<>();
				al.add(orbiters[i]);
				children.put(centers[i], new ArrayList<>(al));
			}
		}
//		System.out.println(bodies.size());
//		System.out.println(centers.length);
//		System.out.println(children.size());
//		System.out.println(parent.size());
		OrbitTree inf = new OrbitTree(children, parent);
		System.out.println(inf.total_weight(bodies));
		
//		System.out.println(parent.get("YOU") + " " + parent.get("SAN"));
		System.out.println(inf.dist(parent.get("YOU"), parent.get("SAN")));
	}

}
