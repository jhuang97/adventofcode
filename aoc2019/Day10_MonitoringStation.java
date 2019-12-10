package adventOfCode;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.Comparator;

public class Day10_MonitoringStation {
	
	public static boolean[][] importArray(String s) {
		String[] strs = s.split("N");
		int ysize = strs.length;
		int xsize = strs[0].length();
		boolean[][] map = new boolean[ysize][xsize];
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				map[iy][ix] = strs[iy].charAt(ix) == '#';
			}
		}
		return map;
	}
	
	public static void printMap(boolean[][] b) {
		for (int iy = 0; iy < b.length; iy++) {
			String a = "";
			for (int ix = 0; ix < b[0].length; ix++) {
				if (b[iy][ix])
					a += "#";
				else
					a += ".";
			}
			System.out.println(a);
		}
	}
	
	public static int numAstVisible(boolean[][] b, int x0, int y0) {
		int ysize = b.length;
		int xsize = b[0].length;
		int count = 0;
		
		boolean[][] c = new boolean[ysize][xsize];
		
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				if (!(ix == x0 && iy == y0)) {
					if (b[iy][ix] && astVisible(b, x0, y0, ix, iy)) {
						count++;
						c[iy][ix] = true;
					}
				}
			}
		}
		return count;
	}
	
	public static boolean astVisible(boolean[][] b, int x0, int y0, int xa, int ya) {
		int dx = xa - x0;
		int dy = ya - y0;
		int sx = (int) Math.signum(dx);
		int sy = (int) Math.signum(dy);
		int magx = Math.abs(dx);
		int magy = Math.abs(dy);
		
		int mgcd = 0;
		int pmagx = 0;
		int pmagy = 0;
		if (sx != 0 && sy != 0) {
			mgcd = gcd(magx, magy);
			pmagx = magx / mgcd;
			pmagy = magy / mgcd;
			
		} else if (sx != 0 && sy == 0) {
			mgcd = magx;
			pmagx = 1;
			pmagy = 0;
		} else if (sx == 0 && sy != 0) {
			mgcd = magy;
			pmagy = 1;
			pmagx = 0;
		} else {
			return false; // can't see itself
		}
		
//		System.out.println("xa ya sx sy " + xa + " " + ya + " " + sx + " " + sy);
//		if (magx == 1 || magy == 1)
//			return true;
		
//		if (xa == 4 && ya == 4) {
//			System.out.println("mgcd " + mgcd + ", pmagx " + pmagx + ", pmagy " + pmagy);
//		}
		
		for (int n = 1; n < mgcd; n++) {
			if (b[y0 + sy*pmagy*n][x0 + sx*pmagx*n])
				return false;
		}
		return true;
	}
	
	static int gcd(int a, int b) {
	    while (b > 0) {
	        int temp = b;
	        b = a % b; // % is remainder
	        a = temp;
	    }
	    return a;
	}
	
	public static int maxAst(boolean[][] b) {
		int maxSoFar = 0;
		int ysize = b.length;
		int xsize = b[0].length;
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				if (b[iy][ix]) {
					int nAst = numAstVisible(b, ix, iy);
					if (nAst > maxSoFar) {
						maxSoFar = nAst;
	//					System.out.println("ix iy nAst " + ix + " " + iy + " " + nAst);
					}
				}
			}
		}
		return maxSoFar;
	}
	
	public static int[] maxAstLoc(boolean[][] b) {
		int maxSoFar = 0;
		int[] maxLoc = new int[2];
		int ysize = b.length;
		int xsize = b[0].length;
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				if (b[iy][ix]) {
					int nAst = numAstVisible(b, ix, iy);
					if (nAst > maxSoFar) {
						maxSoFar = nAst;
						maxLoc[0] = ix;
						maxLoc[1] = iy;
	//					System.out.println("ix iy nAst " + ix + " " + iy + " " + nAst);
					}
				}
			}
		}
		return maxLoc;
	}
	
	public static int[][] getLaserOrder(boolean[][] b, int x0, int y0) {
		int ysize = b.length;
		int xsize = b[0].length;
		boolean[][] isPrimitive = new boolean[ysize][xsize];
		int countPrimitive = 0;
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				if (!(ix == x0 && iy == y0)) {
					int dx = ix - x0;
					int dy = iy - y0;
					int magx = Math.abs(dx);
					int magy = Math.abs(dy);
					if (gcd(magx, magy) == 1) {
						countPrimitive++;
						isPrimitive[iy][ix] = true;
					}
				}
			}
		}
//		return isPrimitive;
		int[][] primPairs = new int[countPrimitive][2];
		int pidx = 0;
		for (int iy = 0; iy < ysize; iy++) {
			for (int ix = 0; ix < xsize; ix++) {
				if (isPrimitive[iy][ix]) {
					int dx = ix - x0;
					int dy = iy - y0;
					primPairs[pidx][0] = dx;
					primPairs[pidx][1] = dy;
					pidx++;
				}
			}
		}
		Arrays.sort(primPairs, Comparator.comparingDouble(a -> -Math.atan2(a[0], a[1])));
		
		return primPairs;
	}
	
	public static int[][] laserRevolve(boolean[][] b, int x0, int y0) {
		int[][] primPairs = getLaserOrder(b, x0, y0);
		int[][] targCoords = new int[primPairs.length][2];
		ArrayList<Integer> removeIdx = new ArrayList<>();
		for (int i = 0; i < primPairs.length; i++) {
			int[] removeLoc = astRemoveLocation(b, x0, y0, primPairs[i]);
			targCoords[i] = removeLoc.clone();
			if (!(removeLoc[0] == 0 && removeLoc[1] == 0)) {
				removeIdx.add(i);
			}
		}
		int[][] targCoordsSel = new int[removeIdx.size()][];
		for (int i = 0; i < removeIdx.size(); i++) {
			targCoordsSel[i] = targCoords[removeIdx.get(i)].clone();
		}
		return targCoordsSel;
	}
	
	public static int[] astRemoveLocation(boolean[][] b, int x0, int y0, int[] primPair) {
		int dx = primPair[0]; int dy = primPair[1];
		int ysize = b.length;
		int xsize = b[0].length;
		int xcurr = x0 + dx;
		int ycurr = y0 + dy;
		while (true) {
			if (xcurr >= xsize || xcurr < 0 || ycurr >= ysize || ycurr < 0) {
				return new int[]{0,0};
			}
			if (b[ycurr][xcurr]) {
				return new int[]{xcurr, ycurr};
			}
			xcurr += dx;
			ycurr += dy;
		}
	}
	
	public static void laserDestroyAll(boolean[][] b, int x0, int y0) {
		int count = 1;
		boolean done = false;
		
		while (!done) {
			int[][] removedAsts = laserRevolve(b, x0, y0);
			for (int[] coords : removedAsts) {
//				System.out.println(count + " " + Arrays.toString(coords));
				if (count == 200) {
					System.out.println(coords[0]*100 + coords[1]);
				}
				count++;
				b[coords[1]][coords[0]] = false;
			}
			if (removedAsts.length == 0) done = true;
		}
	}

	public static void main(String[] args) {
		String in = ".#..#N.....N#####N....#N...##";
//		in = ".#..##.###...#######N##.############..##.N.#.######.########.#N.###.#######.####.#.N#####.##.#.##.###.##N..#####..#.#########N####################N#.####....###.#.#.##N##.#################N#####.##.###..####..N..######..##.#######N####.##.####...##..#N.#####..#.######.###N##...#.##########...N#.##########.#######N.####.#.###.###.#.##N....##.##.###..#####N.#.#.###########.###N#.#.#.#####.####.###N###.##.####.##.#..##";
//		in = ".#....#####...#..N##...##.#####..##N##...#...#.#####.N..#.....#...###..N..#.#.....#....##";
		in = "#.#.###.#.#....#..##.#....N.....#..#..#..#.#..#.....#N.##.##.##.##.##..#...#...#N#.#...#.#####...###.#.#.#.N.#####.###.#.#.####.#####.N#.#.#.##.#.##...####.#.##.N##....###..#.#..#..#..###.N..##....#.#...##.#.#...###N#.....#.#######..##.##.#..N#.###.#..###.#.#..##.....#N##.#.#.##.#......#####..##N#..##.#.##..###.##.###..##N#..#.###...#.#...#..#.##.#N.#..#.#....###.#.#..##.#.#N#.##.#####..###...#.###.##N#...##..#..##.##.#.##..###N#.#.###.###.....####.##..#N######....#.##....###.#..#N..##.#.####.....###..##.#.N#..#..#...#.####..######..N#####.##...#.#....#....#.#N.#####.##.#.#####..##.#...N#..##..##.#.##.##.####..##N.##..####..#..####.#######N#.#..#.##.#.######....##..N.#.##.##.####......#.##.##";
		boolean[][] map = importArray(in);
		printMap(map);
//		System.out.println(gcd(5,0));
		System.out.println(maxAst(map));
		int[] mloc = maxAstLoc(map);
		System.out.println(Arrays.toString(mloc));
//		printMap(numAstVisible(map, 3, 4));
//		System.out.println(Arrays.deepToString(getLaserOrder(map, 3,3)));
		
		laserDestroyAll(map, mloc[0], mloc[1]);
	}

}
