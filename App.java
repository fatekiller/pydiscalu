package liuchenfei;


import java.util.ArrayList;
import java.util.Scanner;

/**
 * Hello world!
 *
 */
public class App 
{

    static ArrayList<Rect> rects=new ArrayList<Rect>();
    public static void main( String[] args )
    {
        buildRects();
        int max=0;
        for (int i = 0; i <rects.size() ; i++) {
            int count=1;
            for (int j = 0; j <rects.size() ; j++) {
                if(isCollapsed(rects.get(i),rects.get(j))){
                    count++;
                }
            }
            if(count>max){
                max=count;
            }
        }
        System.out.println(max);
    }


    public static void buildRects(){
        Scanner in=new Scanner(System.in);
        short n=in.nextShort();
        for (int i = 0; i <n ; i++) {
            Rect r=new Rect();
            r.leftX=in.nextInt();
            rects.add(r);
        }
        in.nextLine();
        for (int i = 0; i <n ; i++) {
            Rect r=rects.get(i);
            r.leftY=in.nextInt();
        }
        in.nextLine();
        for (int i = 0; i <n ; i++) {
            Rect r=rects.get(i);
            r.rightX=in.nextInt();
        }
        in.nextLine();
        for (int i = 0; i <n ; i++) {
            Rect r=rects.get(i);
            r.rightY=in.nextInt();
        }
    }

    public static boolean isCollapsed(Rect r,Rect m){
        if(r.leftX<m.leftX&&r.leftY<m.rightY&&r.rightX>m.leftX&&r.rightY>m.rightY){
            return true;
        }
        if(r.leftX<m.rightX&&r.leftY<m.rightY&&r.rightX>m.rightX&&r.rightY>m.rightY){
            return true;
        }
        if(r.leftX<m.leftX&&r.leftY<m.leftY&&r.rightX>m.leftX&&r.rightY>m.leftY){
            return true;
        }
        if(r.leftX<m.rightX&&r.leftY<r.rightY&&r.rightX>m.rightX&&r.rightY>m.leftY){
            return true;
        }
        return false;
    }
}

class Rect{
    int leftX;
    int leftY;
    int rightX;
    int rightY;
}
