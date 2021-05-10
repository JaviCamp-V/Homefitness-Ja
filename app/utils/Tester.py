
from Workout import Workout,BicepCurls



filename="C:\\Users\\NAVARLEE PETERS UWI\\Videos\\New Dataset\\elbow flare.mkv"

trainer=BicepCurls(220)
print(trainer.export())
out=trainer.video(filename)
print(out)


