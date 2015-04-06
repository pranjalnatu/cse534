package pkg534project;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;

/**
 * @author pranjalnatu
 */
public class ExtractIPs {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        File traceFile = new File("/Users/pranjalnatu/Desktop/download.txt");
        BufferedReader br = new BufferedReader(new FileReader(traceFile));
        ArrayList<String> IPAddrs = new ArrayList<String>();

        String line = br.readLine();
        int lastSeenDst = 0;
        int matchIndexDst = 0;
        
        int lastSeenFrom = 0;
        int matchIndexFrom = 0;
        
        int lastSeenRTT = 0;
        int matchIndexRTT = 0;
        
        String toMatchDst = "dst_addr";
        String toMatchFrom = "from";
        String toMatchRTT = "rtt";
                    
        int fromCt = 0;

        for (int i = 0; i < line.length(); i++) {
            boolean isMatchDst = line.substring(lastSeenDst, i).toLowerCase().contains(toMatchDst.toLowerCase());
            
            if (isMatchDst) {
                matchIndexDst = line.indexOf(toMatchDst, i-9);
                lastSeenDst = i + 1;

                int startOfIP = -1, endOfIP = -1;
                String extracted = null;

                for (int j = matchIndexDst; j < line.length(); j++) {
                    if (line.charAt(j) == ':') {
                        startOfIP = j + 2;
                        break;
                    }
                }

                for (int j = startOfIP; j < line.length(); j++) {
                    if (line.charAt(j) == '\"') {
                        endOfIP = j;
                        break;
                    }
                }

                if(IPAddrs.size() > 0)
                {
                    String prev = IPAddrs.get(IPAddrs.size()-1);
                    String prevSub = prev.substring(0, prev.length()-1);
                    IPAddrs.remove(IPAddrs.size()-1);
                    IPAddrs.add(prevSub);
                }
                
                
                extracted = line.substring(startOfIP, endOfIP);
                IPAddrs.add(extracted + ";");
                
                fromCt=0;
            }
            
            boolean isMatchFrom = line.substring(lastSeenFrom, i).toLowerCase().contains(toMatchFrom.toLowerCase());

            if (isMatchFrom) {
                matchIndexFrom = line.indexOf(toMatchFrom, i-5);
                lastSeenFrom = i + 1;

                int startOfIP = -1, endOfIP = -1;
                String extracted = null;

                for (int j = matchIndexFrom; j < line.length(); j++) {
                    if (line.charAt(j) == ':') {
                        startOfIP = j + 2;
                        break;
                    }
                }

                for (int j = startOfIP; j < line.length(); j++) {
                    if (line.charAt(j) == '\"') {
                        endOfIP = j;
                        break;
                    }
                }

                extracted = line.substring(startOfIP, endOfIP);
                String current = IPAddrs.get(IPAddrs.size()-1);
                IPAddrs.remove(IPAddrs.size()-1);
                               
                
                if(fromCt == 0)
                {
                    IPAddrs.add(current + extracted + ";");
                }
                else if(fromCt > 0)
                {
                    IPAddrs.add(current + extracted + ",");
                }
                
                fromCt++;

            }
            
            boolean isMatchRTT = line.substring(lastSeenRTT, i).toLowerCase().contains(toMatchRTT.toLowerCase());

            if (isMatchRTT) {
                matchIndexRTT = line.indexOf(toMatchRTT, i-4);
                lastSeenRTT = i + 1;

                int startOfRTT = -1, endOfRTT = -1;
                String extracted = null;

                for (int j = matchIndexRTT; j < line.length(); j++) {
                    if (line.charAt(j) == ':') {
                        startOfRTT = j + 1;
                        break;
                    }
                }

                for (int j = startOfRTT; j < line.length(); j++) {
                    if (line.charAt(j) == ',') {
                        endOfRTT = j;
                        break;
                    }
                }

                extracted = line.substring(startOfRTT, endOfRTT);
                String current = IPAddrs.get(IPAddrs.size()-1);
                IPAddrs.remove(IPAddrs.size()-1);
                IPAddrs.add(current + extracted + ";");
            }

        }

        if(IPAddrs.size() > 0)
        {
            String prev = IPAddrs.get(IPAddrs.size()-1);
            String prevSub = prev.substring(0, prev.length()-1);
            IPAddrs.remove(IPAddrs.size()-1);
            IPAddrs.add(prevSub);
        }
        
        
        PrintWriter writer = new PrintWriter("/Users/pranjalnatu/Desktop/extraced_IP_with_RTT.csv", "UTF-8");
        
        for (int i = 0; i < IPAddrs.size(); i++) {
            writer.println(IPAddrs.get(i));
        }
        
        writer.close();
        
    }
}
