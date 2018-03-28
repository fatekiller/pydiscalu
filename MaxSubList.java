package net.liuchenfei.ch4;

import javafx.scene.chart.PieChart;
import net.liuchenfei.utils.DataReader;

import java.io.IOException;

/**
 * Created by liuchenfei on 2018/1/31.
 */
public class MaxSubList {
    public static Integer[] data={13,-3,-25,20,-3,-16,-23,18,20,-7,12,-5,-22,15,-4,7};

    public static Integer[] data2={-10,-1,-2,-3,-4,-5,-6,-7,-8};

    public static Result CrossResult(int begin,int mid,int end,Integer[] A){
        Result r=new Result();
        int leftMax=Integer.MIN_VALUE;
        int leftSum=0;
        r.left=mid;
        for (int i = mid; i >=begin ; i--) {
            leftSum+=A[i];
            if(leftSum>leftMax){
                leftMax=leftSum;
                r.left=i;
            }
        }
        int rightMax=Integer.MIN_VALUE;
        int rightSum=0;
        r.right=mid+1;
        for (int i = mid+1; i <=end ; i++) {
            rightSum+=A[i];
            if(rightSum>rightMax){
                rightMax=rightSum;
                r.right=i;
            }
        }
        r.result=leftMax+rightMax;
        return r;
    }

    public static Result MaxSubII(int begin,int end,Integer[] A){
        Result r=new Result();
        r.result=Integer.MIN_VALUE;
        for (int i = 0; i <A.length ; i++) {
            int sum=0;
            for (int j = i; j <A.length ; j++) {
                sum+=A[j];
                if(sum>r.result){
                    r.result=sum;
                    r.left=i;
                    r.right=j;
                }
            }
        }
        return r;
    }

    /**
     * 这个是线性时间的，主要原理是这样，从左到右扫描，然后每增加一个元素，就分为两类： 最大子数组包含新增的和不包含新增的
     * @param begin
     * @param end
     * @param A
     * @return
     */
    public static Result MaxSubIII(int begin,int end,Integer[] A){
        Result r=new Result();
        int maxConstBegin=begin;
        int maxConstEnd=begin;
        int maxNoConstBegin=begin;
        int maxNoConstEnd=begin;
        int maxConsist=A[begin];
        int maxNoConsist=A[begin];
        boolean isConst=true;
        for (int i = 1; i <end ; i++) {
            int temNoConst=Integer.MIN_VALUE;
            if(isConst){
                temNoConst=maxNoConsist+A[i];
            }
            //当前的单独最大
            if(A[i]>maxNoConsist&&A[i]>temNoConst){
                maxNoConstEnd=i;
                maxNoConsist=A[i];
                maxNoConstBegin=i;
                isConst=true;
            }else if(isConst&&temNoConst>maxNoConsist&&temNoConst>A[i]){
                //当前加上一个最大
                maxNoConstEnd=i;
                maxNoConsist=temNoConst;
                isConst=true;
            }else {
                isConst=false;
            }

            int temConst=maxConsist+A[i];
            //当前加上一个最大
            if(temConst>A[i]){
                maxConstEnd=i;
                maxConsist=temConst;
                //当前的单独就最大
            }else{
                maxConstEnd=i;
                maxConsist=A[i];
                maxConstBegin=i;
            }
            if(maxConsist>maxNoConsist){
                maxNoConsist=maxConsist;
                maxNoConstBegin=maxConstBegin;
                maxNoConstEnd=maxConstEnd;
                r.result=maxConsist;
                r.left=maxConstBegin;
                r.right=maxConstEnd;
            }else{
                r.result=maxNoConsist;
                r.left=maxNoConstBegin;
                r.right=maxNoConstEnd;
            }
        }
        return r;
    }

    public static Result MaxSub(int begin,int end,Integer[] A){
        int k=1000;
        if(begin!=end){
//            if(end-begin<k){
//                long beginTime=System.currentTimeMillis();
//                Result r= MaxSubII(begin,end,A);
//                System.out.println("time cost:"+(System.currentTimeMillis()-beginTime));
//               return r;
//            }
            int mid=(begin+end)/2;
            Result lr=MaxSub(begin,mid,A);
            Result rr=MaxSub(mid+1,end,A);
            Result cr=CrossResult(begin,mid,end,A);
            if(lr.result>rr.result&&lr.result>cr.result){
                return lr;
            }
            if(rr.result>lr.result&&rr.result>cr.result){
                return rr;
            }
            return cr;
        }else {
            Result r=new Result();
            r.left=r.right=begin;
            r.result=A[begin];
            return r;
        }
    }

    public static void main(String[] args) {
        try {

            Integer[] fileData= DataReader.readData("data/maxSubList.csv",150);
            //Integer[] fileData= MaxSubList.data;
            System.out.println(fileData.length);
            long begin=System.currentTimeMillis();
            System.out.println(MaxSubII(0,fileData.length-1,fileData));
            System.out.println("n2:"+(System.currentTimeMillis()-begin));
            long begin2=System.currentTimeMillis();
            System.out.println(MaxSub(0,fileData.length-1,fileData));
            System.out.println("lgn:"+(System.currentTimeMillis()-begin2));
//            long begin3=System.currentTimeMillis();
//            System.out.println(MaxSubIII(0,fileData.length-1,fileData));
//            System.out.println("n:"+(System.currentTimeMillis()-begin3));
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
class Result{
    int left;
    int right;
    int result;

    @Override
    public String toString() {
        return "Result{" +
                "left=" + left +
                ", right=" + right +
                ", result=" + result +
                '}';
    }
}
