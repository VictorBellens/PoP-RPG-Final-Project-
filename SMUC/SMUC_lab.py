import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf

from statsmodels.stats.outliers_influence import variance_inflation_factor
from sklearn.model_selection import train_test_split
from statsmodels.stats.outliers_influence import OLSInfluence
from statsmodels.nonparametric.smoothers_lowess import lowess

filename = "EcomExpense.csv"

data = pd.read_csv(filename, index_col=0)
train, test = train_test_split(data, test_size=0.25, random_state=2023)
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
    ols_resid_plots(model)


def ols_resid_plots(model):
    # Generate the residual values
    residuals = model.resid
    standarized_residuals = OLSInfluence(model).resid_studentized_internal
    fitted_values = model.fittedvalues
    leverage = OLSInfluence(model).hat_matrix_diag

    # Set up the figure and the subplots
    fig, axs = plt.subplots(nrows=3, ncols=3, figsize=(15, 15))

    axs[0, 0].scatter(fitted_values, residuals, alpha=0.5)
    axs[0, 0].axhline(y=0, color='blue', linestyle='--')
    axs[0, 0].set_xlabel('Fit values')
    axs[0, 0].set_ylabel('Residuals')

    # Add a regression line to the scatterplot
    smooth_data = lowess(residuals, fitted_values)
    axs[0, 0].plot(smooth_data[:, 0], smooth_data[:, 1], color='red', alpha=0.5, lw=2)

    # Top-right: QQ plot for standarized residuals
    sm.graphics.qqplot(standarized_residuals, ax=axs[0, 1], line='45')

    # Bottom-left: Fit values vs Squared Root of Standarized residuals
    axs[1, 0].scatter(fitted_values, np.sqrt(np.abs(standarized_residuals)), alpha=0.5)
    axs[1, 0].set_xlabel('Fit values')
    axs[1, 0].set_ylabel('square root(|Standarized residuals|)')

    # Add a Lowess smoother line that fits the best with the data
    smooth_data = lowess(np.sqrt(np.abs(standarized_residuals)), fitted_values)
    axs[1, 0].plot(smooth_data[:, 0], smooth_data[:, 1], color='brown', alpha=0.5)

    # Bottom-right: Residuals vs Leverage plot
    axs[1, 1].scatter(leverage, standarized_residuals, alpha=0.5)
    axs[1, 1].set_xlabel('Leverage')
    axs[1, 1].set_ylabel('Standarized residuals')

    nobs = model.nobs
    p = len(model.params)
    cd = OLSInfluence(model).cooks_distance
    idx = np.where(cd[0] > 0.5)[0]
    for i in idx:
        axs[1, 1].annotate('', xy=(leverage[i], standarized_residuals[i]),
                           xytext=(leverage[i] + 0.05, standarized_residuals[i]),
                           arrowprops=dict(arrowstyle='->', lw=1.5, color='red', alpha=0.5))
        axs[1, 1].annotate(i, xy=(leverage[i], standarized_residuals[i]),
                           xytext=(leverage[i] + 0.05, standarized_residuals[i]), color='red', alpha=0.5)

    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    model = build_model()
    extract_from_model(model)
    cleaned = dummify_model()
    ols_model(cleaned)
