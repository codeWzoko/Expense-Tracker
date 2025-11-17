import matplotlib.pyplot as plt

class Charts:
    @staticmethod
    def bar_by_category(df):
        plt.figure(figsize=(8,4))
        plt.bar(df['category'], df['total'], color="skyblue")
        plt.xlabel("Category")
        plt.ylabel("Total Spent")
        plt.title("Spending by Category")
        plt.tight_layout()
        plt.show()

    @staticmethod
    def pie_by_month(df):
        plt.figure(figsize=(6,6))
        plt.pie(df['total'], labels=df['month'], autopct='%1.1f%%', startangle=90)
        plt.title("Spending by Month")
        plt.tight_layout()
        plt.show()
