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
public class ExtractASNums {

    public static void main(String[] args) throws FileNotFoundException, IOException {
        File traceFile = new File("/Users/pranjalnatu/Desktop/as.txt");
        BufferedReader br = new BufferedReader(new FileReader(traceFile));
        ArrayList<String> ASPaths = new ArrayList<String>();

        String line = br.readLine();
                         
        while(line != null) {
            
            String toMatchStart = "[";
            String toMatchEnd = "]";
            
            int startIdx = -1;
            int endIdx = -1;
            
            boolean isMatchStart = line.toLowerCase().contains(toMatchStart);
            
            if(isMatchStart)
            {
                startIdx = line.indexOf(toMatchStart, 0);
                
                boolean isMatchEnd = line.toLowerCase().contains(toMatchEnd);
                
                if(isMatchEnd)
                {
                    endIdx = line.indexOf(toMatchEnd, startIdx);
                }
                
                if(startIdx != -1 && endIdx != -1)
                {
                    String path = line.substring(startIdx+1, endIdx);
                    path = path.replaceAll("\\s","");
                    ASPaths.add(path);
                }
                
            }            
            
            line = br.readLine();
        }
                    
        PrintWriter writer = new PrintWriter("/Users/pranjalnatu/Desktop/extraced_ASPath.csv", "UTF-8");
        
        for (int i = 0; i < ASPaths.size(); i++) {
            writer.println(ASPaths.get(i));
        }
        
        writer.close();
        
    }
}
