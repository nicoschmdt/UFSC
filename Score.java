public class Score {
    private String difficulty;
    private String name;
    private int time;

    public Score(){
        this("","",0);
    }
    public Score(String dif, String name, int time){
        set_difficulty(dif);
        set_name(name);
        set_time(time);
    }
    public void set_difficulty(String dif) {
        this.difficulty = dif;
    }
    public String get_difficulty() {
        return this.difficulty;
    }
    public void set_name(String name) {
        this.name = name;
    }
    public String get_name() {
        return this.name;
    }
    public void set_time(int time) {
        this.time = time;
    }
    public int get_time() {
        return this.time;
    }
    @Override
    public String toString() {
    	return "difficulty: "+difficulty+",name: "+name+",time: " + time;
    }
}