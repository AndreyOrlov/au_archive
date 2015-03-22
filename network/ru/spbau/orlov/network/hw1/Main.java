package ru.spbau.orlov.network.hw1;

import java.util.StringTokenizer;

public class Main {

    public static void main(String[] args) {
        if (args.length != 3) {
            System.out.println("usage: program <mask> <ip1> <ip2>");
            System.exit(0);
        }

        StringTokenizer maskTokenizer = new StringTokenizer(args[0], ".");
        StringTokenizer ip1Tokenizer = new StringTokenizer(args[1], ".");
        StringTokenizer ip2Tokenizer = new StringTokenizer(args[2], ".");
        for (int i = 0; i < 4; i++) {
            int mask = Integer.parseInt(maskTokenizer.nextToken());
            int ip1 = Integer.parseInt(ip1Tokenizer.nextToken());
            int ip2 = Integer.parseInt(ip2Tokenizer.nextToken());
            ip1 = mask & ip1;
            ip2 = mask & ip2;
            if (ip1 != ip2) {
                System.out.println("IPs belong to different subnets.");
                System.exit(0);
            }
        }
        System.out.println("IPs belong to one subnet.");
    }
}
