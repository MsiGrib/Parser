namespace DiffTimeOSU
{
    internal class MyFrame
    {
        private static int currentId = 0;

        public int Id { get; }
        public int TimePoint { get; }
        public List<string> KeyPressed { get; }

        public MyFrame(int timePoint, List<string> keyPressed)
        {
            Id = ++currentId;
            TimePoint = timePoint;
            KeyPressed = keyPressed ?? new List<string>();
        }
    }
}
