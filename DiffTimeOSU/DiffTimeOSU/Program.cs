using OsuParsers.Decoders;
using OsuParsers.Enums.Replays;
using OsuParsers.Replays;
using OsuParsers.Replays.Objects;

namespace DiffTimeOSU
{
    internal class Program
    {
        static List<int> CalculateTimeGaps(List<MyFrame> frames)
        {
            List<int> timeGaps = new List<int>();
            void added(ref bool _is, ref int _t1, int _t2)
            {
                _is = false;
                timeGaps.Add(_t2 - _t1);
                _t1 = 0;
            }

            bool isM1 = false;
            bool isM2 = false;
            bool isK1 = false;
            bool isK2 = false;

            int t1M1 = 0;
            int t1M2 = 0;
            int t1K1 = 0;
            int t1K2 = 0;

            foreach (MyFrame frame in frames)
            {
                if (!frame.KeyPressed.Any())
                {
                    if (isM1)
                        added(ref isM1, ref t1M1, frame.TimePoint);
                    if (isM2)
                        added(ref isM2, ref t1M2, frame.TimePoint);
                    if (isK1)
                        added(ref isK1, ref t1K1, frame.TimePoint);
                    if (isK2)
                        added(ref isK2, ref t1K2, frame.TimePoint);
                    continue;
                }

                if (frame.KeyPressed.Contains(StandardKeys.M1.ToString()) && !isM1)
                {
                    isM1 = true;
                    t1M1 = frame.TimePoint;
                }
                else if (!frame.KeyPressed.Contains(StandardKeys.M1.ToString()) && isM1)
                    added(ref isM1, ref t1M1, frame.TimePoint);
                if (frame.KeyPressed.Contains(StandardKeys.M2.ToString()) && !isM2)
                {
                    isM2 = true;
                    t1M2 = frame.TimePoint;
                }
                else if (!frame.KeyPressed.Contains(StandardKeys.M2.ToString()) && isM2)
                    added(ref isM2, ref t1M2, frame.TimePoint);
                if (frame.KeyPressed.Contains(StandardKeys.K1.ToString()) && !isK1)
                {
                    isK1 = true;
                    t1K1 = frame.TimePoint;
                }
                else if (!frame.KeyPressed.Contains(StandardKeys.K1.ToString()) && isK1)
                    added(ref isK1, ref t1K1, frame.TimePoint);
                if (frame.KeyPressed.Contains(StandardKeys.K2.ToString()) && !isK2)
                {
                    isK2 = true;
                    t1K2 = frame.TimePoint;
                }
                else if (!frame.KeyPressed.Contains(StandardKeys.K2.ToString()) && isK2)
                    added(ref isK2, ref t1K2, frame.TimePoint);
            }

            if (isM1)
                timeGaps.Add(frames[frames.Count - 1].TimePoint - t1M1);
            if (isM2)
                timeGaps.Add(frames[frames.Count - 1].TimePoint - t1M2);
            if (isK1)
                timeGaps.Add(frames[frames.Count - 1].TimePoint - t1K1);
            if (isK2)
                timeGaps.Add(frames[frames.Count - 1].TimePoint - t1K2);

            return timeGaps;
        }

        static List<int> CalculateTimeGaps(List<ReplayFrame> frames)
        {
            List<int> timeGaps = [];

            var keyStates = new Dictionary<StandardKeys, int?>
            {
                { StandardKeys.K1, null },
                { StandardKeys.K2, null },
                { StandardKeys.M1, null },
                { StandardKeys.M2, null }
            };

            foreach (var frame in frames.OrderBy(f => f.Time))
            {
                if (frame.StandardKeys is StandardKeys.None or StandardKeys.Smoke)
                {
                    keyStates.Where(s => s.Value.HasValue).ToList().ForEach(s =>
                    {
                        timeGaps.Add(frame.Time - s.Value!.Value);
                        keyStates[s.Key] = null;
                    });

                    continue;
                }

                foreach (var key in Enum.GetValues<StandardKeys>().Except([StandardKeys.None, StandardKeys.Smoke]))
                {
                    if (frame.StandardKeys.HasFlag(key) && !keyStates[key].HasValue)
                        keyStates[key] = frame.Time;
                    else if (!frame.StandardKeys.HasFlag(key) && keyStates[key].HasValue)
                    {
                        timeGaps.Add(frame.Time - keyStates[key]!.Value);
                        keyStates[key] = null;
                    }
                }
            }

            keyStates.Where(s => s.Value.HasValue).ToList().ForEach(s =>
            {
                timeGaps.Add(frames.Last().Time - s.Value!.Value);
                keyStates[s.Key] = null;
            });

            return timeGaps;
        }

        static void Main(string[] args)
        {
            // Path from directory
            const string folderPath = @"C:\\Users\\User\\Desktop\\OSR_OnlyMap";
            List<string> files = new List<string>();
            List<int> timeDiffPressed = new List<int>();
            try
            {
                files = Directory.GetFiles(folderPath).ToList();
            }
            catch (Exception e) 
            {
                Console.WriteLine($"Error: {e.Message}");
                return;
            }

            int progressBarRead = files.Count;
            const int progressBarLengthRead = 70;
            for (int i = 0; i < files.Count; i++)
            {
                try
                {
                    Replay replay = ReplayDecoder.Decode(files[i]);
                    List<ReplayFrame> replayFrames = replay.ReplayFrames;
                    List<MyFrame> myFrames = new List<MyFrame>();

                    foreach (ReplayFrame frame in replayFrames)
                    {
                        List<string> tmp = new List<string>();
                        if (frame.StandardKeys.HasFlag(StandardKeys.M1))
                            tmp.Add(StandardKeys.M1.ToString());
                        if (frame.StandardKeys.HasFlag(StandardKeys.M2))
                            tmp.Add(StandardKeys.M2.ToString());
                        if (frame.StandardKeys.HasFlag(StandardKeys.K1))
                            tmp.Add(StandardKeys.K1.ToString());
                        if (frame.StandardKeys.HasFlag(StandardKeys.K2))
                            tmp.Add(StandardKeys.K2.ToString());
                        myFrames.Add(new MyFrame(frame.Time, tmp));
                    }
                    timeDiffPressed.AddRange(CalculateTimeGaps(myFrames));

                    Console.Clear();
                    double progressPercentage = (double)i / progressBarRead * 100;
                    int filledLength = progressBarLengthRead * i / progressBarRead;
                    Console.Write("[");
                    for (int j = 0; j < progressBarLengthRead; j++)
                        Console.Write(j < filledLength ? "*" : " ");
                    Console.Write($"] {progressPercentage:F2}%");
                    Console.WriteLine($" {i}/{progressBarRead} Read and processing.");
                }
                catch (Exception ex)
                {
                    Console.WriteLine($"Ошибка при чтении файла {files[i]}: {ex.Message}");
                }
            }

            string desktopPath = Environment.GetFolderPath(Environment.SpecialFolder.Desktop);
            const string fileName = "Result.txt";
            string filePath = Path.Combine(desktopPath, fileName);

            using (StreamWriter writer = new StreamWriter(filePath))
            {
                int progressBarWrite = timeDiffPressed.Count;
                const int progressBarLengthWrite = 70;
                for (int i = 0; i < timeDiffPressed.Count; i++)
                {
                    if (i % 100 == 0)
                        Console.Clear();

                    writer.WriteLine(timeDiffPressed[i]);

                    double progressPercentage = (double)i / progressBarWrite * 100;
                    int filledLength = progressBarLengthWrite * i / progressBarWrite;
                    Console.Write("[");
                    for (int j = 0; j < progressBarLengthWrite; j++)
                        Console.Write(j < filledLength ? "*" : " ");
                    Console.Write($"] {progressPercentage:F2}%");
                    Console.WriteLine($" {i}/{progressBarWrite} Write.");
                }
            }
        }
    }
}
