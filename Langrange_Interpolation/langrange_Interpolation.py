import matplotlib.pyplot as plt
from matplotlib.widgets import Button
import math

superscript_map = {
    "0": "⁰",
    "1": "¹",
    "2": "²",
    "3": "³",
    "4": "⁴",
    "5": "⁵",
    "6": "⁶",
    "7": "⁷",
    "8": "⁸",
    "9": "⁹",
    "a": "ᵃ",
    "b": "ᵇ",
    "c": "ᶜ",
    "d": "ᵈ",
    "e": "ᵉ",
    "f": "ᶠ",
    "g": "ᵍ",
    "h": "ʰ",
    "i": "ᶦ",
    "j": "ʲ",
    "k": "ᵏ",
    "l": "ˡ",
    "m": "ᵐ",
    "n": "ⁿ",
    "o": "ᵒ",
    "p": "ᵖ",
    "q": "۹",
    "r": "ʳ",
    "s": "ˢ",
    "t": "ᵗ",
    "u": "ᵘ",
    "v": "ᵛ",
    "w": "ʷ",
    "x": "ˣ",
    "y": "ʸ",
    "z": "ᶻ",
    "A": "ᴬ",
    "B": "ᴮ",
    "C": "ᶜ",
    "D": "ᴰ",
    "E": "ᴱ",
    "F": "ᶠ",
    "G": "ᴳ",
    "H": "ᴴ",
    "I": "ᴵ",
    "J": "ᴶ",
    "K": "ᴷ",
    "L": "ᴸ",
    "M": "ᴹ",
    "N": "ᴺ",
    "O": "ᴼ",
    "P": "ᴾ",
    "Q": "Q",
    "R": "ᴿ",
    "S": "ˢ",
    "T": "ᵀ",
    "U": "ᵁ",
    "V": "ⱽ",
    "W": "ᵂ",
    "X": "ˣ",
    "Y": "ʸ",
    "Z": "ᶻ",
    "+": "⁺",
    "-": "⁻",
    "=": "⁼",
    "(": "⁽",
    ")": "⁾",
}

tranSuper = str.maketrans(
    "".join(superscript_map.keys()), "".join(superscript_map.values())
)

fig, ax = plt.subplots()
buttonI_ax = plt.axes([0.85, 0.9, 0.135, 0.035])
buttonC_ax = plt.axes([0.85, 0.95, 0.135, 0.035])
plottedList = []
plottedMap = {}  # X : List(Index)
CurveLine = None


def boundPoint(val):
    if val % 1 < 0.25:
        return math.floor(val)
    elif val % 1 > 0.75:
        return math.ceil(val)
    else:
        return math.floor(val) + 0.5


def plotPoint(event):
    if event.inaxes == ax:
        X = boundPoint(event.xdata)
        Y = boundPoint(event.ydata)
        if plottedMap.get(X, "False") == "False":
            plottedMap[X] = {}
            plottedMap[X]["index"] = len(plottedList)
            (plottedMap[X]["line"],) = ax.plot([X], [Y], "o")
            plottedMap[X]["Y"] = Y
            plottedList.append([X, Y])
        else:
            if plottedMap[X]["Y"] == Y:
                plottedList.pop(plottedMap[X]["index"])
                plottedMap[X]["line"].remove()
                del plottedMap[X]
            else:
                plottedList[plottedMap[X]["index"]][1] = Y
                plottedMap[X]["line"].remove()
                plottedMap[X]["Y"] = Y
                (plottedMap[X]["line"],) = ax.plot([X], [Y], "o")

        print([X], [Y])
        fig.canvas.draw()


def init():
    fig.canvas.mpl_connect("button_press_event", plotPoint)
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 20)
    ax.set_xticks(range(0, 21))
    ax.set_yticks(range(0, 21))
    ax.set_xlabel("X-axis")
    ax.set_ylabel("Y-axis")
    ax.set_title("Click on Coords to Create Unique Graph")
    ax.grid(True)

    button1 = Button(buttonI_ax, "Interpolate!")
    button1.on_clicked(on_button_clicked)

    button2 = Button(buttonC_ax, "Clear!")
    button2.on_clicked(clear)

    plt.suptitle("Langrange Interpolation")
    plt.show(block=True)


def on_button_clicked(event):
    if event.inaxes == buttonI_ax:
        if len(plottedList) > 0:
            interpolate()


def clear(event):
    global CurveLine
    global plottedList
    global plottedMap
    global PerPointEquation
    global FinalEquation
    if event.inaxes == buttonC_ax:
        for [i, k] in plottedMap.items():
            if plottedMap[i]["line"] != None:
                plottedMap[i]["line"].remove()
        plottedList.clear()
        plottedMap.clear()
        PerPointEquation.clear()
        FinalEquation.clear()

        if CurveLine != None:
            CurveLine.remove()
            CurveLine = None

        plt.suptitle("Langrange Interpolation")
        ax.set_title("Click on Coords to Create Unique Graph")
        fig.canvas.draw()


PerPointEquation = []
FinalEquation = []


def interpolate():
    global CurveLine
    global plottedList
    if CurveLine != None:
        CurveLine.remove()
        CurveLine = None
    print("-" * 10)
    length = len(plottedList)
    print("Points : ", plottedList)
    PerPointEquation = []
    for i in plottedList:
        tempCoeff = []
        tempDivide = 1
        for k in plottedList:
            if k != i:
                # (x - 2)(x - 3) . . .
                tempDivide = tempDivide * (i[0] - k[0])
                tempCoeff.append(-k[0])

        tempEquation = []
        tempEquation.append(1 * (i[1] / tempDivide))
        for p in range(1, length - 1):
            # a^(length-p) * b^(p)
            result = []
            combination(tempCoeff, 0, len(tempCoeff), p, 1, result)
            tempEquation.append(sum(result, 0) * (i[1] / tempDivide))

        tempEquation.append(math.prod(tempCoeff) * (i[1] / tempDivide))
        PerPointEquation.append(tempEquation)

    FinalEquation = [0] * length
    for i in PerPointEquation:
        for k in range(length):
            FinalEquation[k] = FinalEquation[k] + i[k]
    print("Final Equation : ", FinalEquation)
    print(
        "Result : y = "
        + " ".join(
            [
                f"{'' if FinalEquation[x] < 0 else '+'}{FinalEquation[x]:.2f}x{str(length - x - 1).translate(tranSuper)} "
                for x in range(length - 1)
            ]
        )
        + f" {'' if FinalEquation[length - 1] < 0 else '+'}{FinalEquation[length - 1]:.2f}"
    )
    print("-" * 10)
    plt.suptitle(
        "Result : y = "
        + " ".join(
            [
                f"{'' if FinalEquation[x] < 0 else '+'}{FinalEquation[x]:.2f}x{str(length - x - 1).translate(tranSuper)} "
                for x in range(length - 1)
            ]
        )
        + f" {'' if FinalEquation[length - 1] < 0 else '+'}{FinalEquation[length - 1]:.2f}"
    )
    xpoints = []
    ypoints = []
    for i in range(0, 21):
        tempSum = 0
        for x in range(length):
            tempSum = tempSum + FinalEquation[x] * pow(i, length - x - 1)
        # if tempSum <= 20:
        ypoints.append(tempSum)
        xpoints.append(i)

    (CurveLine,) = ax.plot(xpoints, ypoints, "-")
    fig.canvas.draw()
    # Optional
    # for i in FinalEquation:
    # evaluate Numerator / Denominator


def combination(arr, start, end, r, temp, result):
    if r == 0:
        result.append(temp)
        return
    if start >= end:
        return
    for i in range(start, end):
        if arr[i] == 0:
            result.append(0)
            continue
        temp = temp * arr[i]
        combination(arr, i + 1, end, r - 1, temp, result)
        temp = temp / arr[i]


init()
