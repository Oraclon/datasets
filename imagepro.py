from PIL import Image;
import matplotlib.pyplot as plt;
import math;

class ImageModel:
    def __init__(self):
        self.pixels  : list = [];
        self.metrics : list = [];
        self.target  : int;
        self.imgName : str;
        self.imgPath : str;

class CropArea:
    def __init__(self):
        self.start : int;
        self.end : int;

class ImageData:
    def __init__(self, image: Image):
        self.height        : float;
        self.width         : float;
        self.diagonal      : float;
        self.pixels        : float;
        self.activePixels  : float;
        self.croppedPixels : float;
        self.view          : list;
        self.overalPixels  : float;
        self._firstPixels  : float;

        if image:
            self.AnalyzeImage(image);

    def AnalyzeImage(self, image: Image) -> None:
        self._firstPixels  = list(image.getdata());
        self.overalPixels  = len(self._firstPixels);
        self.view          = self.BuildView(image);
        self.CropEmptySpace(self.view);

    def BuildView(self, image: Image) -> list:
        return [self._firstPixels[z : z + image.width] 
                for z in [x for x in range(0, self.overalPixels, image.height)]];

    def GetActivePixels(self, pixels : list) -> int:
        activePixels : int = 0;
        for pixel in pixels:
            if pixel:
                activePixels += 1;
        return activePixels;

    def __AnalyzeView(self, pixels : list) -> list:
        crop = CropArea();
        for pid, pixel in enumerate(pixels):
            if sum(pixel):
                crop.start = pid;
                break;
        for pid, pixel in reversed(list(enumerate(pixels))):
            if sum(pixel):
                crop.end = pid+1;
                break;
        return pixels[crop.start: crop.end];

    def CropEmptySpace(self, pixels: list):
        cropped            = self.__AnalyzeView(pixels);
        reversed           = list(zip(*cropped));
        self.view          = list(zip(*self.__AnalyzeView(reversed)));
        self.width         = len(self.view[0]);
        self.height        = len(self.view);
        self.diagonal      = math.sqrt(pow(self.width,2)+pow(self.height,2));
        self.pixels        = [pixel for pixels in self.view for pixel in pixels];
        self.activePixels  = self.GetActivePixels(self.pixels);
        self.croppedPixels = len(self.pixels);

class ImageProcess:
    def __init__(self, imgPath: str) -> ImageModel:
        self.data = ImageModel();
        _pi = (2 * math.pi);
        _imdt         = ImageData(Image.open(imgPath));
        viewFlat = [j for sub in _imdt.view for j in sub]
        
        rightHalf = [[ viewFlat[z] for z in range(x, x + int(_imdt.width / 2))]
            for x in range(int(_imdt.width / 2), len(viewFlat), _imdt.width)];
        rightHalfFlat = [j for sub in rightHalf for j in sub];
        
        self.data.pixels  = _imdt._firstPixels;
        self.data.metrics = [
            _imdt.width,
            _imdt.height,
            _imdt.diagonal,
            (_imdt.width + _imdt.height) * _imdt.diagonal,
            _pi * _imdt.diagonal,
            _pi * ((.5 * _imdt.width) * _imdt.height),
            _imdt.diagonal * _imdt.overalPixels,
            _imdt.width + _imdt.height,
            _pi * (_imdt.width + _imdt.height),
            self.CheckActivePixels(rightHalfFlat) / _imdt.overalPixels
        ];

    def CheckActivePixels(self, array: list):
        active = 0; 
        for pixel in array:
            if pixel: 
                active += 1;
        return active;
