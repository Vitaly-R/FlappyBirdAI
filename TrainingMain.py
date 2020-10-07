from Trainer import Trainer


def main():
    Trainer(gen_size=1000, max_gens=6, mutation_rate=0.1).train()


if __name__ == '__main__':
    main()
