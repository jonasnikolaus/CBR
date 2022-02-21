# Lineare Regression Verformung
            X = arrayzerlegt1[indices]
            y = arrayloesung6[indices]

            nsamples, nx, ny = X.shape
            d2_train_dataset = X.reshape((nsamples, nx*ny))
            d22 = d2_train_dataset.reshape((10, 5))

            nsol, mx, my = y.shape
            e2_train_dataset = y.reshape((nsol, mx*my))
            e22 = e2_train_dataset.reshape((10, 1))

            regverf = LinearRegression().fit(d22, e22)
            #print(regverf.score(d22, e22))
            regverfpred = regverf.predict(input)
            #print(regverfpred)

            # Lineare Regression Spannung
            X1 = arrayzerlegt1[indices]
            y1 = arrayloesung5[indices]

            n1samples, nx1, ny1 = X1.shape
            d21_train_dataset = X1.reshape((n1samples, nx1*ny1))
            d221 = d21_train_dataset.reshape((10, 5))

            n1sol, mx1, my1 = y1.shape
            e21_train_dataset = y1.reshape((n1sol, mx1*my1))
            e221 = e21_train_dataset.reshape((10, 1))

            regspann = LinearRegression().fit(d221, e221)
            #print(regspann.score(d221, e221))
            regspannpred = regspann.predict(input)
            #print(regspannpred)
            