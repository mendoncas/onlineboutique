package imageservice

import (
	"context"
	"os"

	"github.com/ServiceWeaver/weaver"
)

type T interface {
  GetProductImage(ctx context.Context, productId string) ([]byte, error)
}

type impl struct {
  weaver.Implements[T]
  cache map[string][]byte
}

func (s *impl) Init(ctx context.Context) error {
  s.Logger(ctx).Info("Image service started")
  s.cache = make(map[string][]byte)
  return nil
}

func (s *impl) GetProductImage (ctx context.Context, productid string) ([]byte, error){

  if image := s.cache[productid]; image != nil{
    return image, nil
  }

  image, err := os.ReadFile("./imageservice/images/" + productid)
  if err != nil {
    s.Logger(ctx).Error("Falha ao carregar imagem: " + productid)
    s.Logger(ctx).Error(err.Error())
    return nil, err
  }

  s.cache[productid] = image

  return image, nil
}
