import java.util.*;

public class PatternInput {

  public static void main (String[] args){

    ArrayList<String> MondayPattern = new ArrayList<>();
    ArrayList<Boolean> MondayPresent = new ArrayList<>();

    Scanner in = new Scanner(System.in);
    String data = "", temp = "";

    do{
      System.out.println("Enter a time in the HH:MM format (military time):");
      data = in.nextLine();

      if(data.matches("\\d{2}:\\d{2}")){
        System.out.println("Is the item present:");
        temp = in.nextLine();

        if(temp.equals("1")){
          MondayPattern.add(data);
          MondayPresent.add(true);
        }
        else {
          MondayPattern.add(data);
          MondayPresent.add(false);
        }
      }

    }while (!data.equals("-1"));

    for(int i = 0; i < MondayPattern.size(); i++){
      System.out.println(MondayPattern.get(i) + " " + MondayPresent.get(i));
    }

    do {
      System.out.println("What time was item checked:");
      data = in.nextLine();
      System.out.println("Is the item there (1 = present, 0 = false):");
      String data2 = in.nextLine();

      if(data2.equals("-1") || data.equals("-1")){
        break;
      }

      String[] stockArr = new String[MondayPattern.size()];
      stockArr = MondayPattern.toArray(stockArr);

      int i = binarySearch(stockArr, data);

      if (i >= 0){
        //System.out.println(MondayPresent.get(i));

        if((MondayPresent.get(i) && data2.equals("1")) || (!MondayPresent.get(i) && data2.equals("0"))){
          System.out.println("We're good!");
        }
        else{
          System.out.println("There's a problem");
        }
      }
      else{
        i = findSpot(stockArr, data);

        //System.out.println(i);
        //System.out.println(MondayPresent.get(i));

        if(i != -1) {
          //System.out.println(MondayPresent.get(i));
          if((MondayPresent.get(i) && data2.equals("1")) || (!MondayPresent.get(i) && data2.equals("0"))){
            System.out.println("We're good!");
          }
          else{
            System.out.println("There's a problem");
          }
        }
    }

    } while (!data.equals(-1));


  }

  public static int binarySearch(String[] inputArr, String key) {

    int start = 0;
    int end = inputArr.length - 1;
    while (start <= end) {
      int mid = (start + end) / 2;
      if (key.equals(inputArr[mid])) {
        return mid;
      }
      if (key.compareTo(inputArr[mid]) == -1) {
        end = mid - 1;
      } else {
        start = mid + 1;
      }
    }
    return -1;
  }

  public static int findSpot (String[] inputArr, String key){

    int start = 0;

    do{

      //System.out.println(inputArr[start].compareTo(key));
      //System.out.println(inputArr[start+1].compareTo(key));

      if(inputArr[start].compareTo(key) < 0){
        if(inputArr[start + 1].compareTo(key) > 0){
          return start;
        }
      }

      start++;

    }while(start < inputArr.length);

    return -1;

  }

}
