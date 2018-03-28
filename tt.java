    public static int MaxSubIII(int begin,int end,Integer[] A){
        int result=0;
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
                maxNoConsist=A[i];
                isConst=true;
            }else if(isConst&&temNoConst>maxNoConsist&&temNoConst>A[i]){
                //当前加上一个最大
                maxNoConsist=temNoConst;
                isConst=true;
            }else {
                isConst=false;
            }

            int temConst=maxConsist+A[i];
            //当前加上一个最大
            if(temConst>A[i]){
                maxConsist=temConst;
                //当前的单独就最大
            }else{
                maxConsist=A[i];
            }
            if(maxConsist>maxNoConsist){
                maxNoConsist=maxConsist;
                result=maxConsist;
            }else{
                result=maxNoConsist;
            }
        }
        return result;
    }
