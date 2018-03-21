package net.liuchenfei;

import java.util.ArrayList;
import java.util.Scanner;

/**
 * Created by liuchenfei on 2018/3/21.
 */
public class TreeTest {


    static  char[] data=new char[]{'A','B','C'};

    public static void main(String[] args) {
        Scanner scanner=new Scanner(System.in);
        int n=Integer.parseInt(scanner.nextLine());
        data=scanner.nextLine().toCharArray();
        ArrayList<String> result=sortResult(getPostOrder(data,0,n-1));
        for (int i = 0; i <result.size() ; i++) {
            System.out.println(result.get(i));
        }
    }


    public static ArrayList<String> getPostOrder(char[] seq,int begin,int end){
        ArrayList<String> result=new ArrayList<String>();
        if(begin==end){
            result.add(seq[begin]+"");
        }
        if(begin<end){
            for (int i = begin; i <end ; i++) {
                ArrayList<String> leftResult=getPostOrder(seq,begin+1,i);
                leftResult.add("");
                ArrayList<String> rightResult=getPostOrder(seq,i+1,end);
                rightResult.add("");
                for (int j = 0; j < leftResult.size(); j++) {
                    for (int k = 0; k < rightResult.size(); k++) {
                        result.add(leftResult.get(j)+rightResult.get(k)+seq[begin]);
                    }
                }

            }
        }
        ArrayList<String> finalResult=new ArrayList<String>();
        for (int i = 0; i <result.size() ; i++) {
            if(result.get(i).length()==(end-begin+1))
            {
                finalResult.add(result.get(i));
            }
        }
        return finalResult;
    }


    public static ArrayList<String> sortResult(ArrayList<String> strs){
        for (int i = 0; i <strs.size() ; i++) {
            String currentStr=strs.get(i);
            int index=i;
            for (int j = 0; j < strs.size(); j++) {
               if(strs.get(j).compareTo(currentStr)>0){
                   index=j;
                   currentStr=strs.get(j);
               }
            }
            if(index!=i){
                String tmpStr=strs.get(i);
                strs.set(i,currentStr);
                strs.set(index,tmpStr);
            }
        }
        return strs;
    }
}
