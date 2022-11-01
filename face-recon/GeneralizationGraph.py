import matplotlib.pyplot as plot
from ImageHandler import HandlerLineImage


class Grapher:
    def graph(self, histogram: dict, label_img: list[str], save: str = None) -> None:
        values = list(histogram.values())
        x = range(len(values[0]))

        plot.figure(figsize=(15, 10))
        lines = [plot.plot(x, v)[0] for i, v in enumerate(values)]
        empty_labels = ["" for i in lines]
        handler_list = [HandlerLineImage(i) for i in label_img]
        handler_map = dict(zip(lines, handler_list))

        plot.title(save)
        plot.legend(lines, empty_labels,
            handler_map=handler_map, 
            handlelength=1.5, labelspacing=0.0, fontsize=48, borderpad=0.15, loc=2, 
            handletextpad=0.2, borderaxespad=0.15)

        # Save if requested
        if save is not None:
            plot.savefig(save, bbox_inches="tight")

        plot.show()


if __name__ == "__main__":
    pass
