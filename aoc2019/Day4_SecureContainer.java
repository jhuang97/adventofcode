package adventOfCode;

public class Day4_SecureContainer {
	
	public static boolean isOkay(int n) {
		String s = Integer.toString(n);
		char[] cs = s.toCharArray();
		boolean rep = false;
		for (int i = 0; i < cs.length; i++) {
			if (i > 0) {
				if (cs[i] == cs[i-1]) {
					rep = true;
				}
				if (Integer.decode(Character.toString(cs[i])) < Integer.decode(Character.toString(cs[i-1]))) {
					return false;
				}
			}
			
		}
		return rep;
	}
	
	public static boolean isOkay2(int n) {
		String s = Integer.toString(n);
		char[] cs = s.toCharArray();
		int[] hist = new int[10];
		
		for (int i = 0; i < cs.length; i++) {
			hist[Integer.decode(Character.toString(cs[i]))]++;
		}

		for (int i = 0; i < 10; i++) {
			if (hist[i] == 2) 
				return true;
		}
		return false;
	}

	public static void main(String[] args) {
		int count = 0;
		for (int i = 235741; i <= 706948; i++) {
			if (isOkay(i) && isOkay2(i)) count++;
		}
		System.out.println(count);
	}

}
