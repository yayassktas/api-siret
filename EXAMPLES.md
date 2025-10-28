# 💻 Exemples d'Intégration

## Python

```python
import requests

class DocVerifyClient:
    def __init__(self, api_key):
        self.api_key = api_key
        self.base_url = "http://localhost:8000/api/v1"
        self.headers = {
            "X-API-Key": api_key,
            "Content-Type": "application/json"
        }
    
    def verify_siret(self, siret, include_data=True):
        response = requests.post(
            f"{self.base_url}/verify/siret",
            headers=self.headers,
            json={
                "siret": siret,
                "include_company_data": include_data
            }
        )
        return response.json()
    
    def verify_tva(self, numero_tva, verify_vies=True):
        response = requests.post(
            f"{self.base_url}/verify/tva",
            headers=self.headers,
            json={
                "numero_tva": numero_tva,
                "verify_vies": verify_vies
            }
        )
        return response.json()

# Utilisation
client = DocVerifyClient("demo_key_123")
result = client.verify_siret("12345678901234")
print(result)
```

## JavaScript / Node.js

```javascript
const axios = require('axios');

class DocVerifyClient {
  constructor(apiKey) {
    this.apiKey = apiKey;
    this.baseUrl = 'http://localhost:8000/api/v1';
    this.headers = {
      'X-API-Key': apiKey,
      'Content-Type': 'application/json'
    };
  }

  async verifySiret(siret, includeData = true) {
    const response = await axios.post(
      `${this.baseUrl}/verify/siret`,
      {
        siret: siret,
        include_company_data: includeData
      },
      { headers: this.headers }
    );
    return response.data;
  }

  async verifyTva(numeroTva, verifyVies = true) {
    const response = await axios.post(
      `${this.baseUrl}/verify/tva`,
      {
        numero_tva: numeroTva,
        verify_vies: verifyVies
      },
      { headers: this.headers }
    );
    return response.data;
  }
}

// Utilisation
const client = new DocVerifyClient('demo_key_123');
client.verifySiret('12345678901234').then(result => {
  console.log(result);
});
```

## PHP

```php
<?php

class DocVerifyClient {
    private $apiKey;
    private $baseUrl = 'http://localhost:8000/api/v1';
    
    public function __construct($apiKey) {
        $this->apiKey = $apiKey;
    }
    
    public function verifySiret($siret, $includeData = true) {
        $ch = curl_init($this->baseUrl . '/verify/siret');
        
        curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
        curl_setopt($ch, CURLOPT_POST, true);
        curl_setopt($ch, CURLOPT_HTTPHEADER, [
            'X-API-Key: ' . $this->apiKey,
            'Content-Type: application/json'
        ]);
        curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode([
            'siret' => $siret,
            'include_company_data' => $includeData
        ]));
        
        $response = curl_exec($ch);
        curl_close($ch);
        
        return json_decode($response, true);
    }
}

// Utilisation
$client = new DocVerifyClient('demo_key_123');
$result = $client->verifySiret('12345678901234');
print_r($result);
```

## Ruby

```ruby
require 'net/http'
require 'json'

class DocVerifyClient
  def initialize(api_key)
    @api_key = api_key
    @base_url = 'http://localhost:8000/api/v1'
  end

  def verify_siret(siret, include_data: true)
    uri = URI("#{@base_url}/verify/siret")
    
    request = Net::HTTP::Post.new(uri)
    request['X-API-Key'] = @api_key
    request['Content-Type'] = 'application/json'
    request.body = JSON.generate({
      siret: siret,
      include_company_data: include_data
    })

    response = Net::HTTP.start(uri.hostname, uri.port) do |http|
      http.request(request)
    end

    JSON.parse(response.body)
  end
end

# Utilisation
client = DocVerifyClient.new('demo_key_123')
result = client.verify_siret('12345678901234')
puts result
```

## Go

```go
package main

import (
    "bytes"
    "encoding/json"
    "net/http"
)

type DocVerifyClient struct {
    apiKey  string
    baseURL string
}

func NewDocVerifyClient(apiKey string) *DocVerifyClient {
    return &DocVerifyClient{
        apiKey:  apiKey,
        baseURL: "http://localhost:8000/api/v1",
    }
}

func (c *DocVerifyClient) VerifySiret(siret string, includeData bool) (map[string]interface{}, error) {
    payload := map[string]interface{}{
        "siret":                siret,
        "include_company_data": includeData,
    }
    
    jsonData, _ := json.Marshal(payload)
    
    req, _ := http.NewRequest("POST", c.baseURL+"/verify/siret", bytes.NewBuffer(jsonData))
    req.Header.Set("X-API-Key", c.apiKey)
    req.Header.Set("Content-Type", "application/json")
    
    client := &http.Client{}
    resp, err := client.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    
    var result map[string]interface{}
    json.NewDecoder(resp.Body).Decode(&result)
    
    return result, nil
}

func main() {
    client := NewDocVerifyClient("demo_key_123")
    result, _ := client.VerifySiret("12345678901234", true)
    // Utiliser result...
}
```

## Java

```java
import java.net.http.*;
import java.net.URI;
import com.google.gson.Gson;

public class DocVerifyClient {
    private String apiKey;
    private String baseUrl = "http://localhost:8000/api/v1";
    private HttpClient client;
    private Gson gson;

    public DocVerifyClient(String apiKey) {
        this.apiKey = apiKey;
        this.client = HttpClient.newHttpClient();
        this.gson = new Gson();
    }

    public String verifySiret(String siret, boolean includeData) throws Exception {
        var payload = new SiretRequest(siret, includeData);
        String jsonPayload = gson.toJson(payload);

        HttpRequest request = HttpRequest.newBuilder()
            .uri(URI.create(baseUrl + "/verify/siret"))
            .header("X-API-Key", apiKey)
            .header("Content-Type", "application/json")
            .POST(HttpRequest.BodyPublishers.ofString(jsonPayload))
            .build();

        HttpResponse<String> response = client.send(request, 
            HttpResponse.BodyHandlers.ofString());

        return response.body();
    }

    private static class SiretRequest {
        String siret;
        boolean include_company_data;

        SiretRequest(String siret, boolean includeData) {
            this.siret = siret;
            this.include_company_data = includeData;
        }
    }
}

// Utilisation
DocVerifyClient client = new DocVerifyClient("demo_key_123");
String result = client.verifySiret("12345678901234", true);
System.out.println(result);
```

## cURL (Bash)

```bash
#!/bin/bash

API_KEY="demo_key_123"
BASE_URL="http://localhost:8000/api/v1"

# Vérifier SIRET
verify_siret() {
    curl -X POST "$BASE_URL/verify/siret" \
      -H "X-API-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"siret\": \"$1\", \"include_company_data\": true}"
}

# Vérifier TVA
verify_tva() {
    curl -X POST "$BASE_URL/verify/tva" \
      -H "X-API-Key: $API_KEY" \
      -H "Content-Type: application/json" \
      -d "{\"numero_tva\": \"$1\", \"verify_vies\": true}"
}

# Utilisation
verify_siret "12345678901234"
verify_tva "FR12345678901"
```

## Webhooks (pour notifications)

```python
from flask import Flask, request

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    
    if data['event'] == 'company_updated':
        siret = data['siret']
        # Traiter la mise à jour...
        
    return {'status': 'ok'}

if __name__ == '__main__':
    app.run(port=5000)
```

## Intégration No-Code (Zapier)

```javascript
// Exemple de configuration Zapier
{
  "key": "verify_siret",
  "noun": "SIRET Verification",
  "display": {
    "label": "Verify SIRET",
    "description": "Verifies a French SIRET number"
  },
  "operation": {
    "perform": {
      "url": "https://api.docverify.fr/api/v1/verify/siret",
      "method": "POST",
      "headers": {
        "X-API-Key": "{{bundle.authData.api_key}}"
      },
      "body": {
        "siret": "{{bundle.inputData.siret}}"
      }
    }
  }
}
```

---

**Plus d'exemples sur : https://docs.docverify.fr**
