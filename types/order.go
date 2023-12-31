// Copyright 2022 Google LLC
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

package types

import (
	"github.com/ServiceWeaver/weaver"
	"github.com/ServiceWeaver/onlineboutique/cartservice"
	"github.com/ServiceWeaver/onlineboutique/shippingservice"
	"github.com/ServiceWeaver/onlineboutique/types/money"
)

// Order represents a user order.
type Order struct {
	weaver.AutoMarshal
	OrderID            string
	ShippingTrackingID string
	ShippingCost       money.T
	ShippingAddress    shippingservice.Address
	Items              []OrderItem
}

type OrderItem struct {
	weaver.AutoMarshal
	Item cartservice.CartItem
	Cost money.T
}
