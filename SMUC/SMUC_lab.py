import pandas as pd
import statsmodels.api as sm
import statsmodels.formula.api as smf
import numpy as np
from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split

filename = "EcomExpense.csv"

data = pd.read_csv(filename, index_col=0)
train, test = train_test_split(data, test_size = 0.25, random_state = 2023)
train.head()


def build_model():
    predictors_train = pd.read_csv(filename)

    # 2. Build the multiple linear regression model
    x = predictors_train[["Age ", " Items ", "Monthly Income"]]
    y = predictors_train["Total Spend"]

    # Add a constant to the predictor variables
    X = sm.add_constant(x)

    # Fit the model using OLS
    model = sm.OLS(y, X).fit()

    # Get the summary of the model
    print(model.summary())

    # 3. Evaluate the model
    print(f"RSE: {model.mse_resid ** 0.5}")
    print(f"Adj. R-squared: {model.rsquared_adj}")
    print(f"F-stat p-value: {model.f_pvalue}")

    # 4. Select the best combination of predictor variables
    # Here we use backward elimination
    cols = list(X.columns)
    pmax = 1

    while len(cols) > 1:
        X_1 = X[cols]
        model = sm.OLS(y, X_1).fit()
        p_values = model.pvalues
        pmax = max(p_values)
        feature_with_pmax = p_values.idxmax()

        if pmax > 0.05:
            cols.remove(feature_with_pmax)
        else:
            break

    selected_features = cols
    print(f"Selected features: {selected_features}")

    # Check for multi-collinearity
    X_selected = X[selected_features]
    vif = pd.DataFrame()
    vif["Features"] = X_selected.columns
    vif["VIF"] = [variance_inflation_factor(X_selected.values, i) for i in range(X_selected.shape[1])]
    print(vif)
    return model


def extract_from_model(model):
    # We need to calculate or extract this information from the model object
    sse = model.ssr
    rse = np.sqrt(model.mse_resid)  # it is also = np.sqrt(sse/n-2), being n = 3 in this case
    mean_error = (rse / train["Total Spend"].mean()) * 100

    print("SSE:", round(model.ssr, 3))
    print("RSE:", round(np.sqrt(model.mse_resid), 3))
    print("Mean Error:", round(mean_error, 3))


def dummify_model():
    global train, test
    train = pd.get_dummies(train, columns=['Gender', 'City Tier'], drop_first=True)
    train.columns = train.columns.str.strip()

    train.columns = train.columns.str.strip()

    train.columns = train.columns.str.replace('y I', 'y_I')
    train.columns = train.columns.str.replace('n I', 'n_I')
    train.columns = train.columns.str.replace('n T', 'n_T')
    train.columns = train.columns.str.replace("y T", "y_T")
    train.columns = train.columns.str.replace("r 2", "r_2")
    train.columns = train.columns.str.replace("r 3", "r_3")
    train.columns = train.columns.str.replace("l S", "l_S")

    # Display the first few rows of the modified DataFrame
    print(train.head())
    return train


def ols_model(df):
    print(df.columns)
    model_formula = "Total_Spend ~ Age + Items + Monthly_Income + Transaction_Time + " \
                    "Record + Gender_Male + City_Tier_Tier_2 + City_Tier_Tier_3"
    model = smf.ols(formula=model_formula, data=df).fit()
    print(model.summary())


if __name__ == '__main__':
    model = build_model()
    extract_from_model(model)
    cleaned = dummify_model()
    ols_model(cleaned)


